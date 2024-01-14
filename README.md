<p align="center">
  <h1 align="center">koyunotlatan</h1>
  <p align="center">
    <!-- <img src="https://github.com/KGBTR/koyunotlatan/assets/29407019/cb04f067-7fb9-4422-a5f4-c69a3407b361" alt="Pan the Satyr" width="200" title="Pan the Satyr"> -->
    <img src="https://github.com/KGBTR/koyunotlatan/assets/29407019/f873be80-e129-4cd5-ab1d-0d7ebb216dcf" alt="Shepherd Satyr grazing sheeps" width="312" title="Shepherd Satyr grazing sheeps">
  </p>

  <p align="center">
    Ak koyun ak bacağından, kara koyun kara bacağından asılır.<br/>
    Fakat <code>koyunotlatan</code>'ın mahareti, renkten öte, otlatma sanatındadır.
  </p>

  <p align="center">
    <a href="https://reddit.com/user/<BotAccountUsername>">View Demo</a>
    &nbsp;•&nbsp;
    <a href="https://github.com/KGBTR/koyunotlatan/issues">Report Bug</a>
    &nbsp;•&nbsp;
    <a href="https://github.com/KGBTR/koyunotlatan/issues">Request Feature</a>
  </p>
</p>

<p align="center">

  <small>
    Want to support <a href="https://github.com/oldventura">oldventura</a>, who brought us <code><a href="https://github.com/oldventura/koyunkirpan">koyunkirpan</a></code>, you can <a href="https://www.buymeacoffee.com/oldventura" target="_blank">buy him a coffee</a>.
  </small>

  <br>

  <a href="https://www.buymeacoffee.com/oldventura" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy Me A Coffee" width="200">
  </a>
</p>

## Getting Started

### Deploy to Heroku with One-click

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/KGBTR/koyunotlatan)

### Local Installation

1. Clone or download this repository in your project directory

   ```bash
   git clone https://github.com/KGBTR/koyunotlatan.git
   ```

   ```bash
   git clone git@github.com:KGBTR/koyunotlatan.git
   ```

   ```bash
   gh repo clone KGBTR/koyunotlatan
   ```

2. Install dependencies

  Before install dependencies may want to setup virtual enviroment:

  ```sh
  python -m venv .venv
  ```

  ```sh
  # For Sh, Bash, Zsh
  . .venv/bin/activate
  ```

  ```sh
  # For Fish
  . .venv/bin/activate.fish
  ```



  <br/>

   ```sh
   pip install -r requirements.txt
   ```

### Define Reddit Bot Credentials

#### Use `praw.ini`

- Rename `praw.example.ini` to `praw.ini`

  > For MacOSX or linux `mv praw.example.ini praw.ini`

  > For Windows via _Powershell_ `Rename-Item praw.example.ini praw.ini` or via _CMD_ `rename praw.example.ini praw.ini`

or

#### Use `enviroment variables`

Define `BOT_` prefixed enviroment variables defined in [`.env.example`](.env.example)

For `CMD`:

```cmd
set BOT_USERNAME=BotUsername
```

For `PowerShell`:

```powershell
$Env:BOT_USERNAME = "BotUsername"
```

For `Bash` and `Zsh`:

```bash
export BOT_USERNAME=BotUsername
```

For `Fish`:

```fish
set -Ux BOT_USERNAME BotUsername
```

## Usage

```bash
python main.py
```

- Collects total of 100 posts from hot and new.
- Selects one random post
- Collects keywords from this post and top comments
- Searches for similar posts
- Collects top 5 comments from similar posts
- Compares keywords from these comments to find the best fit
- Comments the best fit on the selected post

#### Comment on specific post:

```bash
python main.py -u <post_url>
```

```bash
python main.py --url <post_url>
```

or

```bash
python main.py -i <post_id>
```

```bash
python main.py --id <post_id>
```

- Finds the submission on reddit by the post id
- Finds the submission on reddit by the post url
- **Submission by url takes precedence over the submission by id.**
- Collects keywords from this post and top comments
- Searches for similar posts
- Collects top 5 comments from similar posts
- Compares keywords from these comments to find the best fit
- Comments the best fit on the selected post

## How does it work?

At the beginning, I've tried several things for `koyunkirpan`. But none of the solutions were good enough. They were inconsistent, silly and not suited to the subreddit's context. Then, while I was drinking a few beers, I came up with a stupid solution that just worked. I called it "the `koyunkirpan` algorithm". Yes, `koyunkirpan` does not have artifical intelligence, does not use machine learning models and isn't an oracle machine \:\)

Trying to analyze text context was amazingly hard because of the diversity of the Turkish language. But the semantic of the text was always related to its syntax! So, I wrote a simple algorithm that searched through reddit for keywords in the source text. Here I've used a special search combination for reddit where keywords in the source text were combined together in some kind of a disjunctive normal form (DNF). The highest results always include most of the keywords in some sense. After that, the algorithm collects comments similar to the source text and collects their replies. After ranking the results, it just picks a reply and return this as the response to the source text. Simple but highly suited for a community!

Here's an example of the idea. Imagine you're asking me a question and I don't know the answer but I'm trying to look like I know the answer. So, I go to a university and wander around searching for people that ask similar questions to my original question. I listen to professors' answers, collect them, and then decide on an answer by ranking them. After that I return and just give you the selected answer.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

`koyunkirpan` is not a piece of software nor a product. It's a living piece of art that can be seen as the collective consciousness of users from [r/KGBTR](https://reddit.com/r/KGBTR). Each day, `koyunkirpan` continues to amaze more people as he imitates comments made by real people.

Distributed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) license. See [`LICENSE`](LICENSE) for more information.
