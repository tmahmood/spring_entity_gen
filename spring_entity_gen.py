#!/usr/bin/env python
# encoding: utf-8

import sys
import os.path

MY_PATH = os.path.dirname(os.path.realpath(__file__))
ENTITY_FILE = MY_PATH + '/entity_template.txt'
REPO_FILE = MY_PATH + '/repository_template.txt'
CTRL_FILE = MY_PATH + '/controller_template.txt'
AUDIT_MODEL_FILE = MY_PATH + '/audit_model_template.txt'


def write_from_template(replacements, template, output):
    template_content = None
    with open(template) as fp:
        template_content = fp.read()
    with open(output, 'w') as fp:
        try:
            fp.write(template_content % replacements)
        except TypeError as e:
            print(replacements)
            print(template_content)
            raise e
        except Exception as e:
            print(template)
            print(replacements)
            raise e


def main():
    """
    Entry point
    """
    replacements = {}
    class_name = sys.argv[1]
    replacements['package_name'] = sys.argv[2]
    try:
        other_opts = sys.argv[3:]
    except IndexError:
        other_opts = []
    java_src_package_path = 'src/main/java/%s' % sys.argv[2].replace('.', '/')
    model_path = java_src_package_path + '/models'
    repo_path = java_src_package_path + '/repositories'
    os.makedirs(java_src_package_path, exist_ok=True)
    os.makedirs(model_path, exist_ok=True)
    os.makedirs(repo_path, exist_ok=True)
    # make it camel case
    jcn = class_name.title().replace(' ', '')
    replacements['java_class_name'] = jcn
    # make it snake case
    ssc = class_name.lower().replace(' ', '_')
    ssc_plurel = class_name.lower().replace(' ', '_') + 's'
    replacements['sql_snake_case'] = ssc_plurel
    replacements['sql_snake_case_single'] = ssc
    # write the model template
    model_path_with_name = '{}/{}.java'.format(model_path, jcn)
    write_from_template(replacements, ENTITY_FILE, model_path_with_name)
    repo_path_with_name = '{}/{}Repository.java'.format(repo_path, jcn)
    write_from_template(replacements, REPO_FILE, repo_path_with_name)
    if 'skp_cnt' not in other_opts:
        controller_path = java_src_package_path + '/controllers'
        os.makedirs(controller_path, exist_ok=True)
        ctrl_path_w_name = '{}/{}Controller.java'.format(controller_path, jcn)
        write_from_template(replacements, CTRL_FILE, ctrl_path_w_name)
    if not os.path.exists(model_path + "AuditMode.java"):
        write_from_template(replacements, AUDIT_MODEL_FILE, f'{model_path}/AuditModel.java')


msg = """Parameters missing: %s <class_name> <package_name> [skp_cnt]"""
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(msg % sys.argv[0].split('/').pop())
    else:
        main()
