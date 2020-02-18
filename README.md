# Verify Tweet

Fake tweet images can be generated using a preset meme template from websites like: [TweetGen](https://www.tweetgen.com/), [Prank Me Not](http://www.prankmenot.com/?twitter_tweet) and [Simitator](http://simitator.com/generator/twitter/tweet) . Verification of such tweets takes a manual work to find the user, scroll through their timeline and matching. A viral fake tweet image can prove crucial at a time.

A fake tweet screenshot looks very convincing, misleading the general public. For example:

|Tweet 1             |  Tweet 2 |
|:-------------------------:|:-------------------------:|
|![alt text](https://i.imgur.com/gG1RYiR.png "Tweet 1") | ![alt text](https://i.imgur.com/eTKpOFY.png "Tweet 2")|

Verify Tweet attempts to resolve the problem by letting users upload such tweet screenshots and verify if the user actually tweeted or not. A combination of Image processing, Natural language processing as well as Twitter Search API makes this possible.

## Installation

### Prerequisites

- Install [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract/wiki#installation) and add to PATH.
- Install [ImageMagick](https://imagemagick.org/script/download.php) and add to PATH.
- Python >= 3.6

Installing via pip:

```sh
pip install verifytweet
```

Or via pipenv:

```sh
pipenv install verifytweet
```

## Usage

Quickstart

```sh
verifytweet -f <path_to_image_file>
```

Help

```sh
verifytweet --help
```

## License

Verify Tweet is released under GNU Affero General Public License v3.0.

## Future features

- [ ] Support for Image links
- [ ] Support for Tweets with replies
