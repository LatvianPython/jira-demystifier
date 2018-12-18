import cherrypy
from jira import JIRA
import json
import tenjin
from tenjin.helpers import *
from tenjin.html import *
import os


class CherryApp(object):

    def __init__(self):
        with open('app_config.json', mode='r', encoding='utf-8') as app_config_file:
            self.config = json.loads(app_config_file.read())

        self.jira = JIRA(self.config['jira_url'])
        self.engine = tenjin.Engine()


    @cherrypy.expose()
    def index(self):
        issues = []
        for issue in self.jira.search_issues(self.config['jql']):
            descriptors = []
            for descriptor in self.config['descriptors']:
                try:
                    field = issue.raw
                    for key in descriptor['field_path']:
                        field = field[key]
                except TypeError:
                    field = descriptor['default']
                descriptors.append((descriptor['label'], field))
            issues.append({'issue_color': 'grey',
                           'issue_key': issue.key,
                           'summary': issue.fields.summary,
                           'descriptors': descriptors})
        html = self.engine.render('templates/issues.pyhtml', {'issues': issues})
        return html

if __name__ == '__main__':
    with open("cherrypy_config.json", "r") as cherrypy_config_file:
        config = json.loads(cherrypy_config_file.read())

    for path in config:
        try:
            config[path]['tools.staticfile.filename'] = os.getcwd().replace('\\', '\\\\') + \
                                                        config[path]['tools.staticfile.filename']
        except KeyError:
            pass

    cherrypy.quickstart(CherryApp(), '/', config)
