# python_emailer_practice
A repository for practicing using python to programatically send emails, focused on existing in an API.

## To send emails yourself

### 1. Download Poetry (for python project management)

### 2. Install the package locally
```bash
$ poetry install
```

### 3. Set environment variables in a `.env` file

The file `example.env` contains all of the varaibles you should set.

### 4. Run
If your virtual environment is not active, then from the root directory (where this README and the pyproject.toml is) run:  
```bash
$ poetry run send_email
```

If your virtual environment is active, just run:  
```
$ send_email
```

## TODO List

Get Emailing to work
- [X] create a free email with some service like gmail/outlook
- [X] use the traditional user/pass to send a "Hello World" email


## Experimenting
Play with the libraries and write down anything below for future reference (I may never write anything here.)


#### Sources:  
A lot of this code I did not come up with on my own. Below are projects I copied/changed code from:

- https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/config.py
