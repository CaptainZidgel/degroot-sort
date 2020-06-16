echo "Making Windows CLI file"
cxfreeze cli.py --target-name degroot --target-dir dist/cli --include-modules=dsort,vserv,index
echo "Making Windows UI file"
cxfreeze ui.py --target-name degroot --target-dir dist/ui --include-modules=dsort,vserv
