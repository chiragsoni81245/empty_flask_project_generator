import subprocess
import os
import sys


given_path = sys.argv[2]

if given_path[-1]=="\\" or given_path[-1]=="/":
	given_path = given_path[:len(given_path)-1]

system = ["windows","linux"][os.name!="nt"]

if system=="linux":
	project_name = "/{}".format(sys.argv[1])
else:
	project_name = "\\{}".format(sys.argv[1])	

root_path = given_path + project_name + "_v1.0_"


def run_command( command ):
	p1 = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if p1.returncode==0:
		print( p1.stdout.decode() )
		return p1
	else:
		print( p1.stderr.decode() )
		exit()


def make_folder( path ):
	print("****** Folder is created at '{}' ******".format(path))
	return run_command( ["mkdir",path] )


def make_file( path, content="" ):
	try:
		with open(path,"w") as f:
			f.write( content )
		print("****** File is created at '{}' ******".format(path))

	except:
		print("Error in file Writing")
		exit()


def make_virtual_env( path ):
	try:
		import virtualenv
	except:
		if system=="linux":
			p1 = subprocess.run(["pip3", "install", "virtualenv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			p1 = subprocess.run(["pip", "install", "virtualenv"],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		if p1.returncode!=0:
			print( p1.stderr.decode() )
			exit()
	
	if system=="linux":
		p2 = subprocess.run(["python3","-m","virtualenv",path+"/venv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
		p2 = subprocess.run(["python","-m","virtualenv",path+"\\venv"],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	if p2.returncode==0:
		print("****** Virtualenv is successfully created ******")
		return p2 
	else:
		print( p2.stderr.decode() )


def make_alias( root_dir_path, venv_path ):
	if system=="linux":
		alias = 'alias {}="cd {} && subl {} && source {}/bin/activate"'.format(project_name.lower()[1:],root_path, root_path, venv_path)  
		
		with open( "{}/.bashrc".format(given_path) ,"a") as f:
			f.write('\n{}'.format(alias))

		p1 = os.system("/bin/sh ~/.bashrc")
		
		if p1!=0:
			print( "Error in reloading of bashrc file" )
			exit()
		else:
			print("****** Alias is successfully created ******")
	else:
		pass


if system=="linux":
	make_folder( root_path  )
	make_folder( root_path + project_name )
	make_folder( root_path + project_name + "/app" )
	make_folder( root_path + project_name + "/app/static" )
	make_folder( root_path + project_name + "/app/template" )
else:
	make_folder( root_path  )
	make_folder( root_path + project_name )
	make_folder( root_path + project_name + "\\app" )
	make_folder( root_path + project_name + "\\app\\static" )
	make_folder( root_path + project_name + "\\app\\template" )

init_file_content='''from flask import flask

app = Flask(__name__)

from app import routes
'''

routes_file_content ='''from app import app
'''

run_file_content = "from app import app"

if system=="linux":
	make_file( root_path + project_name + "/app/__init__.py", init_file_content )

	make_file( root_path + project_name + "/app/routes.py", routes_file_content )

	make_file( root_path + project_name + "/run.py", run_file_content )
	
	make_virtual_env( root_path )

	make_alias( root_path, root_path+"/venv" )
else:
	make_file( root_path + project_name + "\\app\\__init__.py", init_file_content )

	make_file( root_path + project_name + "\\app\\routes.py", routes_file_content )

	make_file( root_path + project_name + "\\run.py", run_file_content )

	make_virtual_env( root_path )

	make_alias( root_path, root_path+"\\venv" )
