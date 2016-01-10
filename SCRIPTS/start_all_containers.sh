#!/bin/bash
SECONDS=0
for container in $(lxc-ls --fancy | awk '{print $1}' | tail -n +3 ); do
  lxc-start -n $container && echo "$container started"
done
duration=$SECONDS
echo "The script ran for $(($duration / 60)) minutes and $(($duration % 60)) seconds."
