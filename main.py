#!/usr/bin/env python
#
# This script generates an index of evernote notes in markdown format
# @author Bruno Paz <brunopaz@sapo.pt>
#

import os
import sys
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.edam.type.ttypes import NoteSortOrder
from jinja2 import Environment, FileSystemLoader, Template
from slugify import slugify
from colorama import Fore, Back

reload(sys)
sys.setdefaultencoding('utf8')

OUTPUT_DIR = 'build/'
MAX_NOTES = 1000

def main():

    evernote_auth_token = None;

    while not evernote_auth_token:
        evernote_auth_token = raw_input(Fore.YELLOW + 'Enter your Evernote Developer token (generate it at https://www.evernote.com/api/DeveloperToken.action):' + Fore.RESET)

    print_info("Logging in to Evernote")
    client = EvernoteClient(token=evernote_auth_token, sandbox=False)

    # get the Evernote User.
    user = client.get_user_store().getUser()

    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()

    print_info("Found " + len(notebooks) + " notebooks")

    # iterates over all notebooks to get the notes.
    for notebook in notebooks:
        notes = process_notebook(notebook, note_store, user)
        write_to_file(notebook.name, notes)

    print_info("Finished")

def process_notebook(notebook, note_store, user):

    print_info("Processing notebook:" + notebook.name)

    note_filter = NoteFilter(order=NoteSortOrder.TITLE)
    note_filter.notebookGuid = notebook.guid
    result_spec = NotesMetadataResultSpec(includeTitle=True)
    result_list = note_store.findNotesMetadata(note_filter, 0, MAX_NOTES, result_spec)

    notes = []
    for note in result_list.notes:
        notes.append({
            'title': note.title,
            'link':  generate_note_link(user, note)
        })

    return notes

def generate_note_link(user, note):
    return "https://www.evernote.com/shard/{shard_id}/nl/{user_id}/{note_guid}".format(shard_id = user.shardId, user_id = user.id, note_guid = note.guid)

def write_to_file(notebook, notes):
    filename = slugify(notebook).replace("-", "_") + ".md"
    env = Environment(loader=FileSystemLoader('.'))

    contents = env.get_template('template.j2').render(
        notebook = notebook,
        notes = notes
    )

    f = open(OUTPUT_DIR + filename, "w")
    f.write(contents)

def print_info(text):
    print Fore.GREEN + text + Fore.RESET

try:
    main()
except KeyboardInterrupt:
    sys.exit(0)
