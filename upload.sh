read -p "Enter name of file to upload (with extention), if you want to do a global upload, type * :" name
if [ "$name" = "*" ]
then
    echo "uploading everything"
    git add *
else
    echo "$name is getting uploaded"
    git add $name
fi
read -p "Enter Changelog: " changes
git commit -m " $changes "
git push origin master