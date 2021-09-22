#!/usr/bin/env python
# encoding: utf-8

import os.path
import sys

import inflect

MY_PATH = os.path.dirname(os.path.realpath(__file__))
ENTITY_FILE = MY_PATH + '/templates/entity_template.txt'
REPO_FILE = MY_PATH + '/templates/repository_template.txt'
CTRL_FILE = MY_PATH + '/templates/controller_template.txt'
AUDIT_MODEL_FILE = MY_PATH + '/templates/audit_model_template.txt'
PROJECTION_FILE = MY_PATH + '/templates/projection_template.txt'
SERVICE_FILE = MY_PATH + '/templates/service_template.txt'
ASSEMBLER_FILE = MY_PATH + '/templates/assembler_template.txt'
PAGE_ASSEMBLER_FILE = MY_PATH + '/templates/page_assembler_template.txt'


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
    if os.path.exists(output):
        return
    with open(output, 'w') as fp:
        fp.write(content)


def write_from_template(replacements, template, output):
    content = make_code_from_template(replacements, template)
    write_to_file(output, content)


def make_nice_names(s):
    return s[:1].lower() + s[1:] if s else ''


def make_java_class_names(input_class_name, replacements):
    """ 
        @param: "Book Author"

        @returns:
            java_class_name: BookAuthor
            camel_case: bookAuthor
            camel_case_plural: bookAuthors
            snake_case_plural: book_authors
            snake_case: book_author
    """
    p = inflect.engine()
    replacements['java_class_name'] = input_class_name.title().replace(' ', '')
    replacements['camel_case'] = make_nice_names(input_class_name).replace(' ', '')
    replacements['camel_case_plural'] = p.plural(replacements['camel_case'])
    replacements['snake_case_plural'] = p.plural(input_class_name.lower().replace(' ', '_'))
    replacements['snake_case'] = input_class_name.lower().replace(' ', '_')


class SpringEntityBuilder(object):

    def __init__(self, java_class_name, package_name) -> None:
        super().__init__()
        self.java_class_name = java_class_name
        self.template_vars = {'package_name': package_name}
        make_java_class_names(java_class_name, self.template_vars)
        code_folder = self.template_vars['snake_case']
        self.java_src_package_path = 'src/main/java/%s' % package_name.replace('.', '/')
        # make paths
        self.model_path = f'{self.java_src_package_path}/{code_folder}'
        self.projection_path = f'{self.java_src_package_path}/{code_folder}'
        self.repo_path = f'{self.java_src_package_path}/{code_folder}'
        self.controller_path = f'{self.java_src_package_path}/{code_folder}'
        self.service_path = f'{self.java_src_package_path}/{code_folder}'
        self.assembler_path = f'{self.java_src_package_path}/{code_folder}'
        self.page_assembler_path = f'{self.java_src_package_path}'
        #
        self.model_path_with_name = '{}/{}.java'.format(
            self.model_path,
            self.template_vars['java_class_name'])
        self.projection_file_with_name = '{}/{}.java'.format(
            self.projection_path,
            self.template_vars['java_class_name'])
        self.repo_path_with_name = '{}/{}Repository.java'.format(
            self.repo_path,
            self.template_vars['java_class_name'])
        self.ctrl_path_w_name = '{}/{}Controller.java'.format(
            self.controller_path,
            self.template_vars['java_class_name'])
        self.service_path_w_name = '{}/{}Service.java'.format(
            self.service_path,
            self.template_vars['java_class_name'])
        self.assembler_path_w_name = '{}/{}ResourceAssembler.java'.format(
            self.assembler_path,
            self.template_vars['java_class_name'])
        self.page_assembler_path_w_name = f'{self.java_src_package_path}/PageResourceBuilder.java'


def generate_from_entity_template(entity_details):
    write_from_template(entity_details.template_vars, ENTITY_FILE, entity_details.model_path_with_name)
    write_from_template(entity_details.template_vars, PROJECTION_FILE, entity_details.projection_file_with_name)


def generate_from_repo_template(entity_details):
    write_from_template(entity_details.template_vars, REPO_FILE, entity_details.repo_path_with_name)


def generate_from_controller_template(entity_details):
    write_from_template(entity_details.template_vars, CTRL_FILE, entity_details.ctrl_path_w_name)
    write_from_template(entity_details.template_vars, SERVICE_FILE, entity_details.service_path_w_name)
    write_from_template(entity_details.template_vars, ASSEMBLER_FILE, entity_details.assembler_path_w_name)
    write_from_template(entity_details.template_vars, PAGE_ASSEMBLER_FILE, entity_details.page_assembler_path_w_name)


def make_directories(entity_details):
    os.makedirs(entity_details.java_src_package_path, exist_ok=True)
    os.makedirs(entity_details.model_path, exist_ok=True)
    os.makedirs(entity_details.repo_path, exist_ok=True)


def main():
    """
    Entry point
    """
    entity_details = SpringEntityBuilder(sys.argv[1], sys.argv[2])
    try:
        other_opts = sys.argv[3:]
    except IndexError:
        other_opts = []
    make_directories(entity_details)
    # write the model template
    generate_from_entity_template(entity_details)
    generate_from_repo_template(entity_details)
    if 'skp_cnt' not in other_opts:
        os.makedirs(entity_details.controller_path, exist_ok=True)
        generate_from_controller_template(entity_details)
    if 'with_audit' in other_opts:
        audit_path = f'{entity_details.java_src_package_path}/AuditModel.java'
        if not os.path.exists(audit_path):
            write_from_template(entity_details.template_vars, AUDIT_MODEL_FILE, audit_path)


msg = """Parameters missing: 
%s <class_name in singular form i.e: "Book Author"> <package_name> [skp_cnt] [with_audit]"""
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(msg % sys.argv[0].split('/').pop())
    else:
        main()
