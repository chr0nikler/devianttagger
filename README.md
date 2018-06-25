
## Deviant Tagger

### Neural network attempting to identify the "kind" of image (i.e. photo, traditional drawing/sketch, or digital art)

### Prereqs

1. Install ruby, most likely any version will work, but I'm using 2.3.1
2. Install bundler via `gem install bundler`
3. Run `bundle`
4. You'll need to have a [Deviant Art app](https://www.deviantart.com/developers/) with a client_id and a client_secret. Set those in your environment variables
as DEVIANTART_ID and DEVIANTART_SECRET

### Running

1. If you don't already have images on your machine, run `fetch_images.rb` to fetch images to your machine before running the other, yet to be made, scripts.
