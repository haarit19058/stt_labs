## Understanding VCS
- repository = it is the storage for our project - it contains all the files an their revision history (.git) folder - can be local or remote
- Commit - a snapshot of the codebase at a time includeing the changes
- Branch - a separate line of development
- Merge - Combine changes from one branch to another
- Remote - remote version of the repo


## Git Basics

**Setting  up git**
Configuring git wiht your name and email
```bash
git config --global user.name "Haarit"
git config --global user.email "haarit19058@gmail.com"
```

Verify the configuration
```bash
git config --list
```

**Initialize a local repo**
create a new folder named "  "
```bash
# make a folder named lab1
mkdir lab1

# go to that folder
cd lab1

# initialize the git
git init

# Add the new file README.md and add some comment
echo "This is the first file for the amazing lab1" > README.md

# add file to the staging area
git add . # add all the files
git add README.md # add only the readme file

# commit the file with a message
git commit -m "First commit of the course"

# view commit history
git log
```


## Working with remote repos
**Connecting to github**
- Created a repository on github named as STT

```bash

# change the name of the current branch name to main
# because github uses main as it master branch
git branch -M main

# link the remote repo with the current repo
git remote add origin https://github.com/haarit19058/softwaretoolsntech

# while pushing for the first time
git push --set-upstream origin main

# Pulling the changes 
git pull origin main
```


## Setup a pylint workflow (via github actions) commit your own code and resolve all errors until a green tick appears

- Go to actions tab under the repo that yo uwant to add pylint
- Then find and select pylint
- It will add the follwoign yaml file aa .github/workflows/pylint.yaml
- Now when ever we push the code it will runt these

```yaml
name: Pylint

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10"]
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pylint
    - name: Analysing the code with pylint
      run: |
        pylint $(git ls-files '*.py')
```



## Learning from pylint

- What happened is that the pylint has very strinct rules and if the code does not follow thaose conventions that it will not allow the cod eto pass through
- No trailing empty lines, snake case in functions, compact notations, not more than 5 nested loops allowed