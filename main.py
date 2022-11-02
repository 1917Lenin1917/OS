from itertools import product
from hashlib import sha256
from string import ascii_lowercase
from time import perf_counter

from multiprocessing import Pool, cpu_count

CHUNKSIZE = 5_000


def bruteforce(words: list[str]) -> list[str]:
    # print(f'Running a process with len={len(words)}')
    hashes = [
        '1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad',
        '3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b',
        '74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f'
    ]
    result = []
    for word in words:
        hash_ = sha256(word.encode('utf-8')).hexdigest()
        #print(hash_)
        if hash_ in hashes:
            result.append(f'{word}: {hash_}')

    return result


def single_thread(words: list[str]) -> list[str]:
    print(f'Running a single thread')
    start = perf_counter()

    results = bruteforce(words)
    print(results)

    end = perf_counter()
    print(f'Bruteforcing took {end - start}s')


def multi_thread_chunks(words: list[str]) -> list[str]:
    print(f'Running multiple threads on {cpu_count()} CPUs')
    start = perf_counter()
    chunks = [words[i:i + CHUNKSIZE] for i in range(0, len(words), CHUNKSIZE)]
    # print(chunks)
    with Pool() as pool:

        results = pool.map(bruteforce, chunks)

        print([*filter(len, results)])

    end = perf_counter()
    print(f'Bruteforcing took {end - start}s')


def main():
    print('Generating combinations!')
    words = [''.join(i) for i in product(ascii_lowercase, repeat=5)]
    print(f'Generated {len(words)} combinations!')

    single_thread(words)
    print('-'*20)
    multi_thread_chunks(words)


if __name__ == '__main__':
    main()
