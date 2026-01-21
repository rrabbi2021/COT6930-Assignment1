# Moments

A photo sharing social networking app built with Python and Flask. The example application for the book *[Flask from Beginner to Advanced: Python Web Engineering Practices](https://helloflask.com/en/book/4)* (《[Flask 从入门到进阶：Python Web 开发工程化实践](https://helloflask.com/book/4)》).

Demo: http://moments.helloflask.com

![Screenshot](demo.png)

## Installation

### Bash (macOS/Linux/Git Bash)

```bash
git clone https://github.com/rrabbi2021/COT6930-Assignment1.git
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt

python -m flask --app app.py init-app
python -m flask --app app.py lorem
python -m flask --app app.py run
```

Open http://127.0.0.1:5000/

Login created by `flask lorem`:

- email: `admin@helloflask.com`
- password: `moments`

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
