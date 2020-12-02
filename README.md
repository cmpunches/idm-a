# IDM/A

IDM/A is an identity management, access management, and session management system.  It creates users, manages what groups they're in, and provides a restful API to authenticate and manage the users.

IDM/A can be a replacement for the primary component in big bulky systems that do the same thing, like LDAP, etc.

# Scripts/Tests

Management scripts and tests exist in the 'exec' directory.  They are executed using the following means:

	$ python3 -m exec.{SCRIPT_NAME}

Like every other piece of IDM/A, the management scripts and tests all assume an execution context / working directory of the project root.


