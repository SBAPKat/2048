git add *
read -p "Enter Changelog: " changes
git commit -m " $changes "
git push origin master