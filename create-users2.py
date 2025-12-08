#!/usr/bin/python3

import os
import re
import sys

# This version of the script adds an interactive "dry-run" mode.
# If the user chooses dry-run, the script only prints what commands
# would run and shows skipped/error lines without changing the system.

def main():
# The script supports a "dry-run" mode, which allows the user to test the
    # program without making any actual changes to the system. When dry-run
    # mode is selected:
    #
    #   - No user accounts are created.
    #   - No passwords are set.
    #   - No users are added to any groups.
    #
    # Instead of running the real system commands, the script prints messages
    # showing exactly which commands *would* have been executed. This makes it
    # safe to verify the logic of the script before performing real changes.
    #
    # We read the Y/N answer from /dev/tty so that the prompt still works even
    # when stdin is redirected from a file (create-users.input). If we did not
    # do this, the first line of the input file would be consumed as the answer.
    # Ask the user if they want to run in dry-run mode (no changes)
    # or normal mode (actually create users and groups).
    # We read from /dev/tty so it still works when stdin is redirected.
    with open('/dev/tty') as tty:
        print("Run in dry-run mode? (Y/N): ", end='')
        mode = tty.readline().strip().upper()

    dry_run = (mode == "Y")

    for line in sys.stdin:
        # Keep the original line for messages, but also work with a stripped version.
        raw_line = line.rstrip("\n")

        # Check if the line starts with '#' (a comment in the input file).
        match = re.match("^#", line)

        # Remove whitespace and split the line into fields using ":".
        fields = line.strip().split(':')

        # If this is a commented line in the input file, skip it.
        # In dry-run mode, print a message that it was skipped.
        if match:
            if dry_run:
                print(f"SKIP (comment line): {raw_line}")
            continue

        # If the line does not have exactly 5 fields, it is not valid input.
        # In dry-run mode, print an error about the bad line.
        if len(fields) != 5:
            if dry_run:
                print(f"ERROR (dry-run): Not enough fields in line: {raw_line}")
            continue

        # Extract the username and password from the first two fields.
        # Build the GECOS (full name) field using "First Last" format.
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # The last field contains a comma-separated list of groups.
        groups = fields[4].split(',')

        # Inform the admin which user account is being created.
        print("==> Creating account for %s..." % (username))

        # Command to create the user account with a home directory and GECOS info.
        create_cmd = "/usr/sbin/useradd -m -c '%s' %s" % (gecos, username)
# If running in dry-run mode, we do not execute the useradd command.
        # Instead, we print out the exact command that would have been run.
        # In normal mode, the real command is executed using os.system().
        if dry_run:
            # In dry-run mode, only show what would be run.
            print(f"DRY-RUN: would run: {create_cmd}")
        else:
            # In normal mode, actually run the useradd command.
            print(create_cmd)
            os.system(create_cmd)

        # Inform the admin that we are setting the password for this user.
        print("==> Setting the password for %s..." % (username))

        # Command to set the password non-interactively by piping it into passwd.
        passwd_cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (
            password,
            password,
            username
        )
# In dry-run mode, we only show the passwd command instead of running it.
        # This prevents any real password changes while still showing what the
        # script would do during a full run.
        if dry_run:
            print(f"DRY-RUN: would run: {passwd_cmd}")
        else:
            print(passwd_cmd)
            os.system(passwd_cmd)

        # Loop over each group that the user should be added to.
       # Group assignments also follow the dry-run rules. In dry-run mode, the
        # script prints the adduser command without executing it. In normal mode,
        # the adduser command is run to place the user into each group.
        for group in groups:
            # A '-' in the group field means "no extra groups", so skip it.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                group_cmd = "/usr/sbin/adduser %s %s" % (username, group)
                if dry_run:
                    print(f"DRY-RUN: would run: {group_cmd}")
                else:
                    print(group_cmd)
                    os.system(group_cmd)


if __name__ == '__main__':
    main()
