from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Generator, NewType, TypeVar, TYPE_CHECKING


type UserData = dict[str, str | int]
type OptUserData = UserData | None


@dataclass
class User:
    user_id: str
    name: str
    age: int

    def __bool__(self) -> bool:
        return bool(self.user_id)


@dataclass
class Person(User):
    pass


def fetch_url(url: str) -> UserData:
   return {
       "user_id": "1234",
       "name": "steve",
       "age": 99,
   }


def get_user_data(user: User) -> OptUserData:
    if not user:
        return None

    data = fetch_url(user.user_id)
    return data


def run_get_user_data() -> None:
    user1 = User("1234", "steve", 99)
    data1 = get_user_data(user1)
    print(f"{user1=} got {data1=}")

    data2: OptUserData

    data2 = data1
    print(f"{user1=} got {data2=}")

    user3 = User("", "", 0)
    data3 = get_user_data(user3)
    print(f"{user3=} got {data3=}")

    user4 = Person("5432", "woz", 1024)
    data4 = get_user_data(user4)
    print(f"{user4=} got {data4=}")


Celsius = NewType("Celsius", float)
Fareng = NewType("Fareng", float)


def convert_c_to_f(temp: Celsius) -> Fareng:
    return Fareng(temp * 9 / 5 + 32)


def gen_temps(start: Celsius) -> Generator[Celsius, None, str]:
    yield start
    val = yield Celsius(start + 10)
    yield Celsius(start + 15)

    return "finish"


def get_max_temp(temps: Iterable[Celsius]) -> Celsius | None:
    if not temps:
        return None

    return max(temps)


def get_first_temp(temps: Sequence[Celsius]) -> Celsius | None:
    if not temps:
        return None

    return temps[0]


def run_convert_c_to_f() -> None:
    temp1 = Celsius(-40.0)
    faren1 = convert_c_to_f(temp1)
    print(f"{temp1=}, {faren1=}, {type(temp1)=}, {type(faren1)=}")

    max_temp1 = get_max_temp([Celsius(-40.0), Celsius(5.1), Celsius(36.0)])
    print(f"{max_temp1=}")

    max_temp2 = get_max_temp([])
    print(f"{max_temp2=}")

    temps3: tuple[Celsius, ...] = (Celsius(-40.0), Celsius(5.1), Celsius(36.0))
    max_temp3 = get_max_temp(temps3)
    print(f"{max_temp3=}")

    temps4 = gen_temps(Celsius(10.0))
    max_temp4 = get_max_temp(temps4)
    print(f"{max_temp4=}")

    first_temp1 = get_first_temp([Celsius(-40.0), Celsius(5.1), Celsius(36.0)])
    print(f"{first_temp1=}")

    first_temp2 = get_first_temp([])
    print(f"{first_temp2=}")

    f_temps3: tuple[Celsius, ...] = (Celsius(-40.0), Celsius(5.1), Celsius(36.0))
    first_temp3 = get_first_temp(f_temps3)
    print(f"{first_temp3=}")

    # f_temps4 = gen_temps(Celsius(10.0))
    # first_temp4 = get_first_temp(f_temps4)
    # print(f"{first_temp4=}")


# T = TypeVar("T")


def get_first_temp_generic[T](temps: Sequence[T]) -> T | None:
    if not temps:
        return None

    return temps[0]


def run_generic() -> None:
    first_temp1 = get_first_temp_generic([Celsius(-40.0), Celsius(5.1), Celsius(36.0)])
    print(f"{first_temp1=}")

    first_temp2: Fareng | None = get_first_temp_generic(
        [Fareng(-40.0), Fareng(5.1), Fareng(36.0)]
    )
    print(f"{first_temp2=}")

    # first_temp3: Celsius | None = get_first_temp_generic(
    #     [Fareng(-40.0), Fareng(5.1), Fareng(36.0)]
    # )
    # print(f"{first_temp3=}")


if __name__ == "__main__":
    print(f"{TYPE_CHECKING=}")

    run_get_user_data()
    print("\n------------\n")

    run_convert_c_to_f()
    print("\n------------\n")

    run_generic()
    print("\n------------\n")
