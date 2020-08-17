welcome_message ='''\
Here is a list of short lessons to get you going. You can read
the extended version of this tutorial on https://gitutor.io/guide/
'''
lessons = {
    'Introduction': {
        'description': 'Learn the basic concepts',
        'content': '''\
The basic concepts of git:

Git is a free and open source distributed version control system

A version control system is a tool that saves checkpoints (called commits) of
a file or a set of files over time. A collection of files tracked by git is
called a repository (or repo).

Git is distributed because it's possible to have copies of a repository on
different machines in which checkpoints are saved independently.
Github is a service for storing repositories that act as a source of truth.

On the next lesson you'll learn the basic workflows for git
Gitutor provides beginner friendly commands that wrap git.
Start by using the simple commands.
On the extended tutorial you'll be shown what happens behind the scenes and
what are the actual git commands being used.
'''
    },
    'Single user workflow': {
        'description': 'One person works on the repo',
        'content': '''\
The first and simplest workflow is a single person working on the repository.

1. Change directory into the root folder of your project

    $cd myProject

2. Initialize your project's folder as a git repo

    $gt init

3. Work on your project

4. Create checkpoint to save your changes

    $gt save

    Repeat from step 3.

Extended lesson: https://gitutor.io/guide/one-branch.html
'''

    },
    'Multiple users workflow': {
        'description': 'Multiple people on the repo',
        'content': '''\
The simplest workflow for colaboration is the following:

1.  Initialize a repository as shown in Single User Workflow
    or download a copy of a repo with the url from the repo's github page
    with the following git command:

    $git clone url-of-github-repo

    For example:

    $git clone https://github.com/artemisa-mx/demoRepository.git

2. Grant or ask for write permisions to the github repo

3. Work on your project

4. Create checkpoint to save changes.

    $gt save

5.  If no conflict occurs go to step 3.

6.  If a merge conflict occurs, gitutor will output the names of the
    conflicted files. Solve the conflicts and then create a checkpoint to save
    the conflict resolution:

    $gt save

    Repeat from step 3

    Else, if you don't want to resolve the conflict right away, defer conflict resolution:

    $gt save --defer-conflicts

    Your checkpoint will only be saved locally.

When creating a checkpoint on step 4, you can alteratively use:

    $gt save -l

This will save the checkpoint only on your local machine and wont download
changes from github, avoiding any conflict. When you are ready to sync your
local and remote repo use the command without the -l flag.


Learn how to grant write permisions and how to resolve conflicts on the
extended version of the lesson : https://gitutor.io/guide/one-branch.html
'''

    },
    'More than a save button': {
        'description': 'Learn the gitutor funcionality',
        'content': '''\
Besides saving your project's development history, gitutor offers more funcionality.

- You can compare your current version with any previous commit with:

    $ gt compare

An interactive menu will appear with a list of the repository’s commits. Select one
of them to display the differences between your current version and that particular commit.

Documentation for this command can be found here: https://gitutor.io/guide/gt-compare.html

- You can go back to a previous version of your project with:

    $ gt goback

An interactive menu will again show a list of the repo's commits. Select one to
return to that previous version. Doing this will create a new commit so you can undo
the going back action and return to where you were before.

Documentation for this command can be found here: https://gitutor.io/guide/gt-goback.html

- You can tell gitutor to ignore certain files and don't keep track of them. 
To achieve this use:

    $ gt ignore

An interactive menu will display all the files and folders inside your current
location, check the ones you don't want tracked by git. If you select a folder,
git won’t track any file or folder inside of it. Uncheck files or folders so git
starts tracking them.

Any ignored files will not be uploaded to the remote repository. Gitutor will automaticaly
remove any file alredy in the remote repository if it was ignored in your local repository. 

Documentation for this command can be found here: https://gitutor.io/guide/gt-ignore.html
'''

    },
    'gt init': {
        'description': 'Learn how the gt init command works',
        'content': '''\
# gt init

When the 'gt init' command is called, gitutor runs the following commands under the hood:

    $ git init

This initializes a hidden folder with the name ".git". Git stores in this folder all the
information concerning commits and the different versions of your project.

Afterwards a README.md file is created and the first commit is done with:

    $ git add .
    $ git commit -m 'First commit'

These git commands will be explained in the 'gt save' lesson.

Next, gitutor creates a new empty repository on your github account. This can be done from 
ithub's website. If the repository is created with the default README.md option, it won’t
be possible to push your local repo.

Once the repo has it's first commit and the github repo is created, a remote is added with: 

    $ git add remote origin https://github.com/user/repo.git

A remote is an url that points to a repository on another machine (in this case on github's
servers).

"Origin" refers to the name assigned to that particular remote repository, it could be a
name of your choosing.

Once the remote is added, the commit is pushed with the -u flag to set this remote as the
upstream:

    $ git push -u

This will set your remote repository as the default place where commits should be pushed
and where you’ll pull the changes from.

## Options

This commands offers an optional flags:

-l
    $ gt init -l
This flag tells gitutor to start only a local repository, so no remote repository will
be created.
'''

    },
    'gt save': {
        'description': 'Learn how the gt save command works',
        'content': '''\
# gt save

This command will execute the following actions under the hood:

First it runs:

    $  git add .

This tells git to include the changes within all the files in your repository to your
next commit. These changes include any modifications to your previously saved files and
any new (untracked) files. 

Next, in order to actually save the changes to the project’s history gitutor runs:

    $ git commit -m “your message” 

You can think of a commit as a checkpoint or a snapshot of your repository’s current
state. It’s important to notice that this command only saves the changes to your local
repository.

Then we need to check if there are any changes in the remote repository with: 

    $ git pull

This updates your local repository with the remote changes. Git will try to merge the
files but if there is a conflict a message will be prompted indicating which files have
the conflict. You’ll need to solve all the conflicts manually and then run gt save again.

Finally, if there are no conflicts, you’ll be able to upload your local commits, or
checkpoints, to your remote repository. To do this, gitutor runs:

    $ git push

As you can see, if you wanted to use git to save your changes in the local and remote
repository, you would have to run these 4 commands every time. Instead “gt save” does
all of this for you with only 1 command.

## Options

This commands offers two optional flags:

-m
    gt save -m "your commit message"
This flag tells gitutor to use the message introduced in the command directly instead
of prompting the user for one.

-l
    gt save -l
This flag tells gitutor to only save the changes in your local repository. This way
nothing is modified in your remote repository.

'''
    },
    'gt compare': {
        'description': 'Learn how the gt compare command works',
        'content': '''\
# gt compare

The "gt compare" command will let you compare the current state of your files with a
commit you previously made with the "gt save" command.

After executing "gt compare", you are prompted with a list of all the previous commits
done to your project. You can navigate the list with the arrow keys and select the
commit you want to compare with the enter key.

When a commit is selected, gitutor runs the following:

    $ git diff <hashOfSelectedCommit>

Gitutor will then show you a string containing all the differences between the current
state of your project and the selected commit. The green text is the one that was added
after the selected commit and the red text is the one deleted after the selected commit. 

If you wanted to do the same using only git, you would have to know the hash of the
commit you want to compare or specify the number of commits behind to compare. Instead
"gt compare" offers a way to easily select the commit you want to compare your project with.

## Options

This commands offers an optional flags:

-h
    $ gt compare -h <hashOfSelectedCommit>
This flag tells gitutor to compare the current state of your project to the commit with
the inputted hash. This command flag is usefull if you already know the hash of the commit
you want to compare instead of going through the whole list of commits.
'''
    },
    'gt goback': {
        'description': 'Learn how the gt goback command works',
        'content': '''\
# gt goback

The "gt goback" command will let you return the state of your files to a commit you
previously made with the "gt save" command.

After executing "gt goback", you are prompted with a list of all the previous commits
done to your project. You can navigate the list with the arrow keys and select the commit
you want your project to go back to.

When a commit is selected, gitutor runs the following:

    $ git diff hashOfSelectedCommit

Gitutor will then show you a string containing all the differences between the current
state of your project and the selected commit. The green text is the one that was added
after the selected commit and the red text is the one deleted after the selected commit. 

If you wanted to do the same using only git, you would have to know the hash of the commit
you want to compare or specify the number of commits behind to compare. Instead "gt compare"
offers a way to easily select the commit you want to compare your project with.

## Options

This commands offers an optional flags:

-c
    $ gt compare hashOfSelectedCommit
This flag tells gitutor to compare the current state of your project to the commit with
the inputted commit. This command flag is usefull if you already know the hash of the
commit you want to compare instead of going through the whole list of commits.
'''
    },
    'gt ignore': {
        'description': 'Learn how the gt ignore command works',
        'content': '''\
# gt ignore

Sometimes there are files inside our local repository that we don't want to upload to
the remote repository, such as keys, passwords or log files. The *.gitignore* file tells
Git which files or folders to ignore. This means that Git won't track any changes made to
those files and that they won't be uploaded to your remote repository.

It's recommended to have a .gitignore file so that when you run

    $ git add .

Git won't upload any unwanted files by mistake. .gitignore  is a plain-text file in which
each line specifies a pattern to ignore. For example: 

* 'hello.*' will match any file or folder whose name begins with hello ('hello.txt',
'hello.log', 'hello.py')

* 'doc/'will match a folder named 'doc' but not a file named 'doc'. When you ignore
a folder, Git will ignore any files or folders inside of it.

* 'main.py' will match any file named exactly 'main.py'.

* '*.csv' will match every csv file in your repository

It's important to note that the .gitignore file specifies intentionally **untracked** files
that Git should ignore. Files already tracked by Git are not affected so if, for example,
you committed a file named 'keys.py' by mistake and later you add this pattern to the
.gitignore file, nothing will happen. That is, the 'keys.py' file will remain in the
remote repo and Git will still track any modifications. 

Gitutor provides an easy way to add files and folders to your .gitignore file so that you
don't have to do it by hand! When you run 

    $ gt ignore

Gitutor will display a list with all the files and folders in your current directory. You
only need to check all the files or folders you want to ignore, or uncheck any previously
ignored file so that Git will begin to track it. 

If you check a file or folder which was previously tracked by Git, Gitutor will run:

    $ git rm --cached <filename>

This will remove said file form Git's tracked files and it will also remove the file from
your remote repository, but not from your local one.

'''
    },
}
