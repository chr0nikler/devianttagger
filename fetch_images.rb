#!/usr/bin/ruby

require "csv"
require "json"
require "httpclient"

class Tag
    attr_accessor :offset, :name, :done

    def initialize(name)
        @offset = 0
        @name = name
        @done = false
    end
end

#
# Class to fetch images
#
# client, connections, images and tags are all class levels
# vars to avoid instantiating multiple ImageFetchers and
# opening too many connections. This is meant to be dirt
# simple, just to get the job done
#
class ImageFetcher
    @@client = HTTPClient.new(
        default_header: {
            "User-Agent" => "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept-Encoding": "compress"
        }
    )
    # Uncomment for debugging requests
    #@@client.debug_dev = $stdout
    @@connections = []
    @@images = []
    @@tags = []
    @@count = 0

    def initialize
        @auth_url = "https://www.deviantart.com/oauth2"
        @api_url = "https://www.deviantart.com/api/v1/oauth2"
        @access_token = ""
    end

    # Asynchronously fetches images of a specific tag
    # Note: not truly async, because check_connections
    # call is made in a blocking manner here, but theoretically
    # check_connections could be spawned in a separate thread
    def fetch_tag(tag)
        begin
            auth_check
            url = "#{@api_url}/browse/tags"
            params = {
                "tag" => tag.name,
                "offset" => tag.offset,
                "access_token" => @access_token
            }
            @@connections << { "connection" => @@client.get_async(url,params), "tag" => tag }
            check_connections
            if(!tag.done)
                fetch_tag(tag)
            end
            @@images
        rescue Exception
            @@count += 1
            puts @@count
        end
    end

    private

    # Performs a check using the current access token
    # to see if a new one is needed before making api calls
    def placebo_check
        placebo = "#{@api_url}/placebo"
        params = {
            "access_token" => @access_token
        }
        res = @@client.get(placebo,params)
        body = JSON.parse(res.body)
        return body["status"] == "success"
    end


    # Fetches access token if needed
    def auth_check
        if !placebo_check
            url = "#{@auth_url}/token"
            params = {
                "grant_type" => "client_credentials",
                "client_id" => ENV["DEVIANTART_ID"],
                "client_secret" => ENV["DEVIANTART_SECRET"]
            }
            res = @@client.get(url,params)
            body = JSON.parse(res.body)
            @access_token = body["access_token"]
        end
    end

    def does_image_apply?(image,tag_name)
        return !image["is_deleted"] &&
            image["is_downloadable"] &&
            !image["content"].nil? &&
            image["category_path"].include?(tag_name)
    end

    # Checks all open connections and process
    # those that have finished
    def check_connections
        while !@@connections.empty?
            @@connections.delete_if do |connection_info|
                if(connection_info["connection"].finished?)
                    res = JSON.load(connection_info["connection"].pop.body)
                    sources = []
                    for result in res["results"]
                        if does_image_apply?(result,connection_info["tag"].name)
                            sources << [result["content"]["src"], connection_info["tag"].name]
                        end
                    end
                    @@images += sources
                    tag = connection_info["tag"]
                    if @@images.select { |i| i[1] == tag.name }.size < 5000
                        tag.offset = res["next_offset"]
                    else
                        tag.done = true
                    end
                    true
                else
                    false
                end
            end
        end
        @@images
    end

end

traditional = Tag.new("traditional")
photography = Tag.new("photography")
#digital_art = Tag.new("digitalart")

imageFetcher = ImageFetcher.new

images = (imageFetcher.fetch_tag(traditional)).uniq
CSV.open("data.csv", "wb") do |csv|
    csv << ["image","tag"]
    images.each do |elem|
        csv << elem
    end
end

images = imageFetcher.fetch_tag(photography)
#images += imageFetcher.fetch_tag(digital_art)

# Because I'm a bad coder an introduced some kind of doubling logic in check_connections
# typical of attempting multithreaded garbage
images = images.uniq

# Writes all images to file of "image,tag"
CSV.open("data.csv", "wb") do |csv|
    csv << ["image","tag"]
    images.each do |elem|
        csv << elem
    end
end
