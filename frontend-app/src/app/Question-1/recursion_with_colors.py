from typing import List, Tuple, Union

Disk = Tuple[int, str]
Move = Tuple[int, str, str]

def can_place(top: Disk, bottom: Disk) -> bool:
    return top[0] < bottom[0] and top[1] != bottom[1]

def is_valid_stack(stack: List[Disk]) -> bool:
    for i in range(len(stack) - 1):
        if not can_place(stack[i + 1], stack[i]):
            return False
    return True

def solve_hanoi(disks: List[Disk]) -> Union[int, List[Move]]:
    moves: List[Move] = []
    rods = {"A": disks[:], "B": [], "C": []}

    def move(n: int, source: str, target: str, aux: str):
        if n == 0:
            return True

        if not move(n - 1, source, aux, target):
            return False

        disk = rods[source].pop()
        rods[target].append(disk)
        if not is_valid_stack(rods[target]):
            return False

        moves.append((disk[0], source, target))

        if not move(n - 1, aux, target, source):
            return False

        return True

    if move(len(disks), "A", "C", "B"):
        return moves
    return -1


if __name__ == "__main__":
    
    disks = [(3, "red"), (2, "blue"), (1, "blue")] 
    result = solve_hanoi(disks)
    print(result)
