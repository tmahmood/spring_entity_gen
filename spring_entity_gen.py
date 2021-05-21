#!/usr/bin/env python
# encoding: utf-8

import sys
import os.path
import inflect

MY_PATH = os.path.dirname(os.path.realpath(__file__))
ENTITY_FILE = MY_PATH + '/entity_template.txt'
REPO_FILE = MY_PATH + '/repository_template.txt'
CTRL_FILE = MY_PATH + '/controller_template.txt'
AUDIT_MODEL_FILE = MY_PATH + '/audit_model_template.txt'

def make_code_from_template(replacements, template):
    template_content = None
    try:
        with open(template) as fp:
            template_content = fp.read()
        return template_content % replacements
    except TypeError as e:
        print(replacements)
        print(template_content)
        raise e
    except Exception as e:
        print(template)
        print(replacements)
        raise e


def write_to_file(output, content):
    with open(output, 'w') as fp:
        fp.write(content)


def write_from_template(replacements, template, output):
    content = make_code_from_template(replacements, template)
    write_to_file(output, content)


def make_java_class_names(input_class_name, replacements):
    """ 
        @param: "Book Author"

        @returns:
            class name: BookAuthor
            table name: book_authors
            java variable name: bookAuthor
            api endpoint: bookAuthors
    """
    func = lambda s: s[:1].lower() + s[1:] if s else ''
    p = inflect.engine()
    replacements['java_class_name'] = input_class_name.title().replace(' ', '')
    replacements['camel_case'] = func(input_class_name).replace(' ', '')
    replacements['camel_case_plural'] = p.plural(replacements['camel_case'])
    replacements['snake_case_plural'] = p.plural(input_class_name.lower().replace(' ', '_'))


class SpringEntityBuilder(object):

    def __init__(self, java_class_name, package_name) -> None:
        super().__init__()
        self.java_class_name = java_class_name
        self.template_vars = {'package_name': package_name}
        make_java_class_names(java_class_name, self.template_vars)
        self.java_src_package_path = 'src/main/java/%s' % package_name.replace('.', '/')
        self.model_path = self.java_src_package_path + '/models'
        self.repo_path = self.java_src_package_path + '/repositories'
        self.controller_path = self.java_src_package_path + '/controllers'
        self.model_path_with_name = '{}/{}.java'.format(
            self.model_path, 
            self.template_vars['java_class_name'])
        self.repo_path_with_name = '{}/{}Repository.java'.format(
            self.repo_path, 
            self.template_vars['java_class_name'])
        self.ctrl_path_w_name = '{}/{}Controller.java'.format(
            self.controller_path,
            self.template_vars['java_class_name'])


def generate_from_entity_template(entityDetails):
    write_from_template(entityDetails.template_vars, ENTITY_FILE, entityDetails.model_path_with_name)


def generate_from_repo_template(entityDetails):
    write_from_template(entityDetails.template_vars, REPO_FILE, entityDetails.repo_path_with_name)


def generate_from_controller_template(entityDetails):
    write_from_template(entityDetails.template_vars, CTRL_FILE, entityDetails.ctrl_path_w_name)


def make_directories(entityDetails):
    os.makedirs(entityDetails.java_src_package_path, exist_ok=True)
    os.makedirs(entityDetails.model_path, exist_ok=True)
    os.makedirs(entityDetails.repo_path, exist_ok=True)


def main():
    """
    Entry point
    """
    entityDetails = SpringEntityBuilder(sys.argv[1], sys.argv[2])
    try:
        other_opts = sys.argv[3:]
    except IndexError:
        other_opts = []
    make_directories(entityDetails)
    # write the model template
    generate_from_entity_template(entityDetails)
    generate_from_repo_template(entityDetails)
    if 'skp_cnt' not in other_opts:
        os.makedirs(entityDetails.controller_path, exist_ok=True)
        generate_from_controller_template(entityDetails)
    auditPath = f'{entityDetails.model_path}/AuditModel.java'
    if not os.path.exists(auditPath):
        write_from_template(entityDetails.template_vars, AUDIT_MODEL_FILE, auditPath)


msg = """Parameters missing: %s <class_name in singular form i.e: "Book Author"> <package_name> [skp_cnt]"""
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(msg % sys.argv[0].split('/').pop())
    else:
        main()
