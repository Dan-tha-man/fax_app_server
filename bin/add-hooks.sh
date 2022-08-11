#!/bin/sh

FAX_DIR=~/repos/fax_server

/bin/rm -f $FAX_DIR/.git/hooks/pre-commit
sudo cp $FAX_DIR/bin/pre-commit $FAX_DIR/.git/hooks/pre-commit
sudo chmod u+x $FAX_DIR/.git/hooks/pre-commit
/bin/rm -f $FAX_DIR/.git/hooks/post-checkout
sudo cp $FAX_DIR/bin/post-checkout $FAX_DIR/.git/hooks/post-checkout
sudo chmod u+x $FAX_DIR/.git/hooks/post-checkout