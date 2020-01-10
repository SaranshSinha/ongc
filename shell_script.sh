#!/bin/bash
function kill_child
{
   tmp=''
   count=1
  # IFS=$' '
   for pro in $(ps -elf |grep $1 |awk '{print $4 " " $5}')
   do
      a=1


      if [ $(( count % 2 )) -eq 0 ]
       then

              if [ $pro -eq $1 ]
                  then
                    dep=$(($2+a))
                    echo "dep is" $dep "child is $tmp parent is $pro"
                    kill_child $tmp $dep
              fi
      fi
      export tmp=$pro
   let "count++"
   #echo $1

   done
   if [ $2 -ne 0 ]
    then
     kill -9 $1

     echo $1 ' killed'
    fi

}
id_test=$(ps -C shell_script1.sh -o pid=)
#id=$(ps -elf|grep shell_script1|awk '{print $4}')
echo $id_test
#echo $id
kill_child $id_test 0
