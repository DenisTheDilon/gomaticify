#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from gomatic import *
import argparse
import sys

def get_users_and_roles(yaml_auth_dict):
    users = yaml_auth_dict.get('users',[])
    roles = yaml_auth_dict.get('roles',[])
    return users, roles

class Authorization(object):
	def __init__(self, element, authorization_dict):
		self.__authorization_dict = authorization_dict
		self.__element = element

	def configure(self):
		self.configure_view_authorization(self.__authorization_dict.get('view', dict()))
		self.configure_operate_authorization(self.__authorization_dict.get('operate', dict()))
		self.configure_admins_authorization(self.__authorization_dict.get('admins', dict()))

	def configure_view_authorization(self, auth_dict):
		if auth_dict:
			users, roles = get_users_and_roles(auth_dict)
			self.__element.set_authorization_profile(ViewUserProfile(users, roles))

	def configure_operate_authorization(self, auth_dict):
		if auth_dict:
			users, roles = get_users_and_roles(auth_dict)
			self.__element.set_authorization_profile(OperateUserProfile(users, roles))

	def configure_admins_authorization(self, auth_dict):
		if auth_dict:
			users, roles = get_users_and_roles(auth_dict)
			self.__element.set_authorization_profile(AdminUserProfile(users, roles))

class Material(object):
	"""docstring for Material"""
	def __init__(self, pipeline, materials_dict):
		self.__pipeline = pipeline
		self.__materials_dict = materials_dict

	def configure(self):
		self.configure_package_materials()\
			.configure_git_materials()\
			.configure_pipeline_materials()

	def configure_package_materials(self):
		map(lambda x: self.__ensure_material(self.__get_package_material(x)), self.__materials_dict.get('package', []))
		return self

	def configure_git_materials(self):
		map(lambda x: self.__ensure_material(self.__get_git_material(x)), self.__materials_dict.get('git', []))
		return self

	def configure_pipeline_materials(self):
		map(lambda x: self.__ensure_material(self.__get_pipeline_material(x)), self.__materials_dict.get('pipeline', []))
		return self

	def __get_git_material(self, material_dict):
		return GitMaterial(material_dict['url'], material_dict.get('branch', None), material_dict.get('material-name', None)\
        	, material_dict.get('auto-update', True), material_dict.get('filter-ignore-patterns', set())\
        	, material_dict.get('dest', None))

	def __get_package_material(self, material_dict):
		return PackageMaterial(package_id=material_dict['ref'])

	def __get_pipeline_material(self, material_dict):
		return PipelineMaterial(material_dict['pipeline-name'], material_dict['stage-name'], \
        	material_dict.get('material-name', None))

	def __ensure_material(self, material):
		self.__pipeline.ensure_material(material)

class EnvironmentVariable(object):
	"""docstring for EnvironmentVariables"""
	def __init__(self, element, variable_dict):
		self.__element = element
		self.__variables_dict = variable_dict

	def configure(self):
		self.set_secure_variable()\
			.set_variable()

	def set_secure_variable(self):
		if self.__variables_dict.get('secure', False):
			self.__element.ensure_encrypted_environment_variables({ self.__variables_dict['name']: \
				self.__variables_dict.get('encrypted-value', None) })
		return self

	def set_variable(self):
		if not self.__variables_dict.get('secure', False):
			self.__element.ensure_environment_variables({ self.__variables_dict['name']: \
	        	self.__variables_dict.get('value', None) })
		return self

class Task(object):
	"""docstring for Task"""
	def __init__(self, job, task_dict):
		self.__job = job
		self.__task_dict = task_dict

	def configure(self):
		map(lambda x: self.configure_exec_tasks(x), self.__task_dict.get('exec', dict()))
		map(lambda x: self.configure_rake_tasks(x), self.__task_dict.get('rake', dict()))
		map(lambda x: self.configure_fetch_artifact_material(x), self.__task_dict.get('fetch-artifact', dict()))

	def configure_exec_tasks(self, exec_task):
		command_and_args = [exec_task['command']]
		for args in exec_task.get('args', []):
			command_and_args.append(args)
		self.__job.add_task(ExecTask(command_and_args, exec_task.get('working-dir', None)\
        	, exec_task.get('runif', 'passed')))

	def configure_rake_tasks(self, rake_task):
		self.__job.add_task(RakeTask(rake_task['target'], rake_task.get('runif', 'passed')))

	def configure_fetch_artifact_material(self, fetch_task):
		self.__job.add_task(FetchArtifactTask(fetch_task['pipeline'], fetch_task['stage'], fetch_task['job']\
        	, FetchArtifactDir(fetch_task['src']), fetch_task.get('dest', None), fetch_task.get('runif', 'passed')))		

class Job(object):
	"""docstring for Job"""
	def __init__(self, stage, job_dict):
		self.__stage = stage
		self.__job_dict = job_dict

	def configure(self):
		self.ensure_job()\
			.set_environment_variables()\
			.set_run_on_all_agents()\
			.set_tasks()\
			.set_tabs()\
			.set_resources()

	def ensure_job(self):
		self.__job = self.__stage.ensure_job(self.__job_dict['name']) 
		return self

	def set_timeout(self):
		if 'timeout' in self.__pipeline_dict:
			self.__job.set_timeout(self.__pipeline_dict['timeout'])
		return self

	def set_environment_variables(self):
		map(lambda x: EnvironmentVariable(self.__job, x).configure(), self.__job_dict.get('environment-variables', []))
		return self

	def set_run_on_all_agents(self):
		self.__job.set_runs_on_all_agents(self.__job_dict.get('run-on-all-agents', False))
		return self

	def set_tasks(self):
		Task(self.__job, self.__job_dict.get('tasks', dict())).configure()
		return self

	def set_tabs(self):
		map(lambda x: self.__job.ensure_tab(Tab(x['name'], x['path'])), self.__job_dict.get('tabs', dict()))
		return self

	def set_resources(self):
		map(lambda x: self.__job.ensure_resource(x), self.__job_dict.get('resources', []))
		return self

class Stage(object):
	"""docstring for Stage"""
	def __init__(self, pipeline, stage_dict):
		self.__pipeline = pipeline
		self.__stage_dict = stage_dict
		
	def configure(self):
		self.ensure_stage()\
			.set_approval()\
			.set_fetch_materials()\
			.set_clean_working_dir()\
			.set_environment_variables()\
			.set_jobs()

	def ensure_stage(self):
		self.__stage = self.__pipeline.ensure_stage(self.__stage_dict['name'])
		return self

	def set_approval(self):
		self.__set_approval_with_authorization(self.__stage_dict.get('approval', dict()))
		self.__set_approval_without_authorization(self.__stage_dict.get('approval', dict()))
		return self

	def set_clean_working_dir(self):
		if self.__stage_dict.get('clean-working-dir', False):
			self.__stage.set_clean_working_dir()
		return self

	def set_fetch_materials(self):
		self.__stage.set_fetch_materials(self.__stage_dict.get('fetch-materials', False))
		return self

	def set_environment_variables(self):
		map(lambda x: EnvironmentVariable(self.__stage, x).configure(), self.__stage_dict.get('environment-variables', []))
		return self

	def set_jobs(self):
		map(lambda x: Job(self.__stage, x).configure(), self.__stage_dict.get('jobs', []))
		return self

	def __set_approval_with_authorization(self, approval_dict):
		if 'authorization' in approval_dict and approval_dict.get('type','') == 'manual':
			stage_auth = approval_dict['authorization']
			users, roles = get_users_and_roles(stage_auth)
			self.__stage.set_has_manual_approval_with_authorization(users, roles)

	def __set_approval_without_authorization(self, approval_dict):
		if not 'authorization' in approval_dict and approval_dict.get('type','') == 'manual':
			self.__stage.set_has_manual_approval()

class PipelineElement(object):
	"""docstring for PipelineBase"""
	def set_stages(self, pipeline, pipeline_dict):
		map(lambda x: Stage(pipeline, x).configure(), pipeline_dict.get('stages', []))

class Template(PipelineElement):
	"""docstring for Template"""
	def __init__(self, configurator, template_dict):
		super(Template, self).__init__()
		self.__configurator = configurator
		self.__template_dict = template_dict

	def configure(self):
		self.ensure_template()\
			.set_authorization()\
			.set_stages()

	def ensure_template(self):
		self.__template = self.__configurator.ensure_replacement_of_template(self.__template_dict['name'])
		return self

	def set_authorization(self):
		Authorization(self.__template, self.__template_dict.get('authorization', dict()))\
			.configure()
		return self

	def set_stages(self):
		super(Template, self).set_stages(self.__template, self.__template_dict)
		return self

class Pipeline(PipelineElement):
	"""docstring for Pipeline"""
	def __init__(self, element, pipeline_dict):
		super(Pipeline, self).__init__()
		self.__element = element
		self.__pipeline_dict = pipeline_dict

	def configure(self):
		self.ensure_pipeline()\
			.set_template()\
			.set_locking()\
			.set_label_template()\
			.set_timer()\
			.set_params()\
			.set_materials()\
			.set_stages()

	def ensure_pipeline(self):
		self.__pipeline = self.__element.ensure_replacement_of_pipeline(self.__pipeline_dict['name'])
		return self

	def set_locking(self):
		if self.__pipeline_dict.get('is-locked', False):
			self.__pipeline.set_automatic_pipeline_locking()
		return self

	def set_label_template(self):
		if 'label-template' in self.__pipeline_dict:
			self.__pipeline.set_label_template(self.__pipeline_dict['label-template'])
		return self

	def set_timer(self):
		timer_dict = self.__pipeline_dict.get('timer', dict())
		if timer_dict:
			self.__pipeline.set_timer(timer_dict['value'], timer_dict.get('only-on-changes', False))
		return self

	def set_params(self):
		params_dict = dict((d['name'], d['value']) for d in self.__pipeline_dict.get('params', dict()))
		if params_dict:
			self.__pipeline.ensure_parameters(params_dict)
		return self

	def set_template(self):
		if 'template' in self.__pipeline_dict:
			self.__pipeline.set_template_name(self.__pipeline_dict['template'])
		return self

	def set_materials(self):
		Material(self.__pipeline, self.__pipeline_dict.get('materials', dict()))\
			.configure()
		return self

	def set_stages(self):
		super(Pipeline, self).set_stages(self.__pipeline, self.__pipeline_dict)
		return self

class PipelineGroup(object):
	"""docstring for PipelineGroup"""
	def __init__(self, configurator, pipeline_group_dict):
		self.__configurator = configurator
		self.__pipeline_group_dict = pipeline_group_dict

	def configure(self):
		self.ensure_pipeline_group()\
			.set_authorization()\
			.set_pipelines()

	def ensure_pipeline_group(self):
		self.__pipeline_group = self.__configurator\
			.ensure_removal_of_pipeline_group(self.__pipeline_group_dict["group"])\
            .ensure_pipeline_group(self.__pipeline_group_dict["group"])
		return self

	def set_authorization(self):
		Authorization(self.__pipeline_group, self.__pipeline_group_dict.get('authorization', dict()))\
			.configure()
		return self

	def set_pipelines(self):
		map(lambda x: Pipeline(self.__pipeline_group, x).configure(), self.__pipeline_group_dict.get('pipelines', []))
		return self

class YamlToGomaticConverter(object):
    def __init__(self,host, username=None, password=None, ssl=False, verify_ssl=True):
        self.__configurator = GoCdConfigurator(HostRestClient(host, username, password, ssl, verify_ssl))

    def convert_from_yaml_file(self,yaml_file):
        f = open(yaml_file, 'r')
        yaml_string = f.read()        
        self.convert_from_yaml_string(yaml_string)
        return self.__configurator;

    def convert_from_yaml_string(self, yaml_string):
        yaml_dict = yaml.load(yaml_string)
        map(lambda x: PipelineGroup(self.__configurator, x).configure(), yaml_dict.get('pipeline-groups', []))
        map(lambda x: Template(self.__configurator, x).configure(), yaml_dict.get('templates', []))
        return self.__configurator;        
#python -m gomaticify --server="10.31.67.169" --username="dodilon" --password="18097011" --yaml_path="/drives/c/Users/DODILON/source/gomaticify/example_yaml.yml" --save_locally=True
def main(args):
    parser = argparse.ArgumentParser(description='Gomaticify is an API for configuring GoCD using Gomatic and YAML file '
                                                 'Run python -m gomaticify to configure a pipeline.')
    parser.add_argument('-s', '--server', help='the GoCD server (e.g. "10.11.12.13" or "my.gocd.com")')
    parser.add_argument('--username', help='the username for the gocd server', default=None)
    parser.add_argument('--password', help='the password for the gocd server', default=None)
    parser.add_argument('--ssl', help='use HTTPS for the connection to the gocd server', dest='ssl', action='store_true', default=False)
    parser.add_argument('--verify_ssl', help='if set the identity of the ssl certificate will be verified.', dest='verify_ssl', action='store_true', default=False)
    parser.add_argument('--yaml_path', help='the path to the YAML file with the GoCD configuration.', default=None)
    parser.add_argument('--yaml_string', help='the YAML formatted string  with the GoCD configuration.', default=None)
    parser.add_argument('--save_locally', help='when True gomaticify save your file locally instead send to GoCD server.', default=False)
    args = parser.parse_args(args)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.yaml_path is None and args.yaml_string is None:
        raise RuntimeError("You need to inform a yaml path or string")

    converter = YamlToGomaticConverter(args.server, args.username, args.password, ssl=args.ssl, verify_ssl=args.verify_ssl)

    go_server = None
    if args.yaml_path is not None:
        go_server = converter.convert_from_yaml_file(args.yaml_path)
    elif args.yaml_string is not None:
        go_server = converter.convert_from_yaml_string(args.yaml_string)

    go_server.save_updated_config(save_config_locally=args.save_locally, dry_run=args.save_locally)

if __name__ == '__main__':
    main(sys.argv[1:])