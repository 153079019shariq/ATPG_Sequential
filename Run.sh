

rm -rf ATPG_output.txt

python Graph_build_c17.py G1 G8 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py G1 G8 sa1
python Graph_build.py
python Podem.py
sleep 1


python Graph_build_c17.py G3 fanout1 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py G3 fanout1 sa1
python Graph_build.py
python Podem.py
sleep 1




python Graph_build_c17.py fanout1 G8 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py fanout1 G8 sa1
python Graph_build.py
python Podem.py
sleep 1



python Graph_build_c17.py fanout1 G9 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py fanout1 G9 sa1
python Graph_build.py
python Podem.py
sleep 1


python Graph_build_c17.py G4 G9 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py G4 G9 sa1
python Graph_build.py
python Podem.py
sleep 1



python Graph_build_c17.py G2 G12 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py G2 G12 sa1
python Graph_build.py
python Podem.py
sleep 1



python Graph_build_c17.py G5 G15 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py G5 G15 sa1
python Graph_build.py
python Podem.py
sleep 1


python Graph_build_c17.py fanout2 G12 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py fanout2 G12 sa1
python Graph_build.py
python Podem.py
sleep 1


python Graph_build_c17.py fanout2 G15 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py fanout2 G15 sa1
python Graph_build.py
python Podem.py
sleep 1



python Graph_build_c17.py fanout3 G16 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py fanout3 G16 sa1
python Graph_build.py
python Podem.py
sleep 1



python Graph_build_c17.py fanout3 G17 sa0
python Graph_build.py
python Podem.py
sleep 1

python Graph_build_c17.py fanout3 G17 sa1
python Graph_build.py
python Podem.py
sleep 1

geany ATPG_output.txt
