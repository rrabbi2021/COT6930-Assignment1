# Moments Demo

![hippo]([https://media3.giphy.com/media/aUovxH8Vf9qDu/giphy.gif](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHBpOTR0enVjd24yMnhvMzJ0Z21heXB2aTdyenk2c2ZxcmZzNG5rdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/EWooQbLD5Tt3vVOtnh/giphy.gif))

## Dependencies

- flask>=3.0.2
- flask-sqlalchemy>=3.1.1
- flask-login>=0.6.3
- flask-dropzone>=1.6.0
- flask-mail>=0.9.1
- flask-wtf>=1.2.1
- flask-whooshee>=0.9.1
- flask-avatars>=0.2.3
- bootstrap-flask>=2.3.3
- python-dotenv>=1.0.1
- pillow>=10.2.0
- pyjwt>=2.8.0
- email-validator>=2.1.0.post1
- torch>=2.0.0
- transformers>=4.36.0

## Installation

### Bash (macOS/Linux/Git Bash)

```bash
git clone https://github.com/rrabbi2021/COT6930-Assignment1.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

flask --app app.py init-db
flask --app app.py lorem
flask --app app.py run
```
IMPORTANT!!! Please make sure to clear browser cache before uploading images, there is an unkown error causing uploads to fail at times.

Open http://127.0.0.1:5000/

Login created by `flask lorem`:

- email: `admin@helloflask.com`
- password: `moments`

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
