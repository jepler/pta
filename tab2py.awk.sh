#!/bin/sh
#//LDIB    *       0100    2       T1      1       0       00FF    /*load immediate
#//1       2       3       4       5       6       7       8

awk -non-decimal-data '
function mask2count(mask) {
    mask = mask+0
    count = 0;
    while(mask >= 1) { count += 1; mask/= 2; }
    return count;
}

/^\/\*/ { $1 = "# "; print; }
/^[A-Z]/ {
    insn=$1; pattern=$2; bits=("0x" $3)+0; mask=("0x" $8)+0;
    bitcount = mask2count(mask);
    $9 = substr($9, 2)
    $1 = $2 = $3 = $4 = $5 = $6 = $7 = $8 = ""

    check = sprintf("I%d", bitcount);
    if(pattern == "\"\"")
        arg = sprintf("\"%s\",", insn);
    else
        arg = sprintf("\"%s %s\",", insn, pattern);
    printf("Insn(%-20s %3s, 0x%04x)\n", arg,  check, bits );
}' "$@"
