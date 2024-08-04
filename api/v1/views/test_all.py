#!/usr/bin/python3

from models.state import State
from models import storage

states_list = []
states = storage.all(State)
for obj in states.values():
    states_list.append(obj.to_dict())

print(states_list)
