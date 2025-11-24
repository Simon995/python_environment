#!/bin/bash
# File: update-submodule-branch.sh
# Since: 2022/10/10
# Desc:
#     update submodule by tag
#     git submodule update --remote failed when branch is a tag
echo "============== Before Upgrade ================"
git submodule sync --recursive && git submodule update --init --recursive --force
git submodule status
echo "============== Run Upgrade ================"
git submodule foreach -q 'git fetch && branch=$(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master) && echo $name $branch && git checkout $branch'
# git submodule foreach -q 'git fetch && git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'
echo "============== After Upgrade ================"
git submodule status