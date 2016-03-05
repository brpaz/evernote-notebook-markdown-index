# Evernote Notebook Markdown Index

This python scripts, allows to Export a List of Notes in each of your Evernote Notebook into Markdown Format.

## Requirements

* python
* pip
* An Evernote account

## Usage

Install the required dependencies using pip

```
sudo pip install -r requirements.txt
```

Execute the main.py script and input your Evernote Developer Token when requested.
If you dont have a Developer token you can generate one [here](https://www.evernote.com/api/DeveloperToken.action)

```
python main.py
```

A markdown file for each of your notebooks will be generated in the build/ folder.
