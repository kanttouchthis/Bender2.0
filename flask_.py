#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from parlai.core.agents import create_agent
from parlai.core.params import ParlaiParser
from parlai.core.script import ParlaiScript, register_script


@register_script('flask_', hidden=True)
class Flask_(ParlaiScript):
    @classmethod
    def setup_args(cls):
        parser = ParlaiParser(True, True)
        return parser

    def chatbot_response(self):
        from flask import request

        data = request.json
        done = data.get("episode_done", False)
        self.agent.observe({'text': data["text"], 'episode_done': done})
        response = self.agent.act()
        return {'response': response['text']}

    def reset(self):
        self.agent.history.reset()
        return {'response': ""}

    def run(self):
        from flask import Flask

        self.agent = create_agent(self.opt)
        app = Flask("parlai_flask")
        app.route("/response", methods=("GET", "POST"))(self.chatbot_response)
        app.route("/reset", methods=("GET", "POST"))(self.reset)
        app.run()


if __name__ == "__main__":
    Flask_.main()