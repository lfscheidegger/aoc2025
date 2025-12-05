import sys

INPUT = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

INPUT = "1-14,46452718-46482242,16-35,92506028-92574540,1515128146-1515174322,56453-79759,74-94,798-971,49-66,601-752,3428-4981,511505-565011,421819-510058,877942-901121,39978-50500,9494916094-9494978970,7432846301-7432888696,204-252,908772-990423,21425-25165,1030-1285,7685-9644,419-568,474396757-474518094,5252506279-5252546898,4399342-4505058,311262290-311393585,1895-2772,110695-150992,567521-773338,277531-375437,284-364,217936-270837,3365257-3426031,29828-36350"

def part1():
    def check(id: int):
        id_str = str(id)
        if len(id_str) % 2:
            return 0
        left = id_str[0:len(id_str)//2]
        right = id_str[len(id_str)//2:]
        if left == right:
            return id
        return 0


    result = 0
    for seq in INPUT.split(","):
        left, right = seq.split("-")
        for id in range(int(left), int(right)+1):
            result += check(id)

    print(result)


def part2():
    def check(id: int):
        id_str = str(id)
        str_len = len(id_str)

        chunk_length = 1
        while chunk_length <= str_len//2:
            if str_len % chunk_length:
                chunk_length += 1
                continue

            base_chunk = id_str[0:chunk_length]
            all_match = True
            for test_chunk_base in range(chunk_length, str_len, chunk_length):
                test_chunk = id_str[test_chunk_base:test_chunk_base+chunk_length]
                if test_chunk != base_chunk:
                    all_match = False

            if all_match == True:
                return id
            chunk_length += 1

        return 0
            
    
    result = 0
    for seq in INPUT.split(","):
        left, right = seq.split("-")
        for id in range(int(left), int(right)+1):
            result += check(id)

    print(result)
    
part2()
