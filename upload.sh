read -p "Type B to create a new branch (in case of uploading error, or in case of multiple people working at the same time) or type R for a regular upload:" regular
if [ "$regular" = "B" ]
then
    echo "selecting Branch Upload"
    read -p "Type name of branch (please use date, or something explicit):" branch_name
    git checkout -b $branch_name
else
    echo "selecting upload to main branch"
    branch_name="master"
fi
echo "uploading"
git add *
read -p "Enter Changelog: " changes
git commit -m " $changes "
git push origin $branch_name
