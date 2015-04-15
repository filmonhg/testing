#!/usr/bin/perl-w


print "Original setting \n";
print "---------------------\n";
my @favorite_swarves=("Grumpy", "Bashful","Sleepy","Dopey","Doc","Happy", "Sneezy");
print @favorite_swarves;
print "****************\n";
print $favorite_swarves[0]."\t".$favorite_swarves[1]."\t".$favorite_swarves[2]."\t".$favorite_swarves[3]."\t".$favorite_swarves[4]."\t".$favorite_swarves[5]."\t". $favorite_swarves[6]."\n";

#alteration #1
print "alteration #1\n";
print "---------------------\n";
shift @favorite_swarves;
print $favorite_swarves[0]."\t".$favorite_swarves[1]."\t".$favorite_swarves[2]."\t".$favorite_swarves[3]."\t".$favorite_swarves[4]."\t".$favorite_swarves[5]."\t". $favorite_swarves[6]."\n";

#alteration #2
print "alteration #2\n";
print "---------------------\n";
push(@favorite_swarves,"Thorin");
print $favorite_swarves[0]."\t".$favorite_swarves[1]."\t".$favorite_swarves[2]."\t".$favorite_swarves[3]."\t".$favorite_swarves[4]."\t".$favorite_swarves[5]."\t". $favorite_swarves[6]."\n";

#alteration #3
print "alteration #3\n";
print "---------------------\n";
reverse @favorite_swarves;
print $favorite_swarves[0]."\t".$favorite_swarves[1]."\t".$favorite_swarves[2]."\t".$favorite_swarves[3]."\t".$favorite_swarves[4]."\t".$favorite_swarves[5]."\t". $favorite_swarves[6]."\n";

#alteration #4
print "alteration #4\n";
print "---------------------\n";
pop @favorite_swarves;
print $favorite_swarves[0]."\t".$favorite_swarves[1]."\t".$favorite_swarves[2]."\t".$favorite_swarves[3]."\t".$favorite_swarves[4]."\t".$favorite_swarves[5]."\t". $favorite_swarves[6]."\n";

#alteration #5
print "alteration #5\n";
print "---------------------\n";
splice(@favorite_swarves,3,0,"Kill");
print $favorite_swarves[0]."\t".$favorite_swarves[1]."\t".$favorite_swarves[2]."\t".$favorite_swarves[3]."\t".$favorite_swarves[4]."\t".$favorite_swarves[5]."\t". $favorite_swarves[6]."\n";

