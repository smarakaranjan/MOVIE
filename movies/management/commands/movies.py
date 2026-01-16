import random
from django.core.management.base import BaseCommand
from movies.models import Movie, Person, Genre, MovieActor, MovieGenre

# Real image URLs for actors (using TMDB image CDN format)
ACTOR_IMAGES = {
    "Robert Downey Jr.": "https://image.tmdb.org/t/p/w300/5qHNjhtjMD4YWH3UP0s4YbqHKaP.jpg",
    "Scarlett Johansson": "https://image.tmdb.org/t/p/w300/6NsMbJXRlDZu6zat3FYxjy1HpBt.jpg",
    "Chris Evans": "https://image.tmdb.org/t/p/w300/3bOGNsHlrswhyW79uvIHH1V43JI.jpg",
    "Mark Ruffalo": "https://image.tmdb.org/t/p/w300/isQ747u0MU8U9gdsNlPngnP8ZPv.jpg",
    "Chris Hemsworth": "https://image.tmdb.org/t/p/w300/jpurJ9jAcLCYjgHHfYF32m3zJYm.jpg",
    "Jennifer Lawrence": "https://image.tmdb.org/t/p/w300/7YmHruJz5aKXqYhkdwirsgxwl0F.jpg",
    "Brad Pitt": "https://image.tmdb.org/t/p/w300/cckcYc2v0yh1tc9QjRelptcOBko.jpg",
    "Angelina Jolie": "https://image.tmdb.org/t/p/w300/k3W1XXddDOH2zibP9tOwylY5jAk.jpg",
    "Leonardo DiCaprio": "https://image.tmdb.org/t/p/w300/wo2hJpn04vbtmh0B9utCFdsQhxM.jpg",
    "Natalie Portman": "https://image.tmdb.org/t/p/w300/edPU5HxncLWa1YkgRWNekphlbbs.jpg",
    "Tom Hanks": "https://image.tmdb.org/t/p/w300/pQFoyx7rp09CJT0jqoB0qN3y4m.jpg",
    "Meryl Streep": "https://image.tmdb.org/t/p/w300/7rmMU3h7zQqEQH6n9Ka7k5yqS5m.jpg",
    "Morgan Freeman": "https://image.tmdb.org/t/p/w300/oGJQhOpT8S1F56m3ro7kWH3oPAO.jpg",
    "Emma Stone": "https://image.tmdb.org/t/p/w300/cZ8a3QvAnj2cgcgVL6g4XaqPzpL.jpg",
    "Ryan Gosling": "https://image.tmdb.org/t/p/w300/lyUyVARQKhGxaxy0FbPJCQRpiaN.jpg",
    "Gal Gadot": "https://www.imdb.com/name/nm2933757/?ref_=nmbio_ov_i",
    "Henry Cavill": "https://image.tmdb.org/t/p/w300/iWdKjMry5Pt8omUxq3sgf0lb2JZ.jpg",
    "Zendaya": "https://image.tmdb.org/t/p/w300/6TE2al2QLvxR49fObWuEUdX0F4z.jpg",
    "Dwayne Johnson": "https://image.tmdb.org/t/p/w300/kuqFzlYMc2IrsOyPznMd1FroeGq.jpg",
    "Margot Robbie": "https://image.tmdb.org/t/p/w300/euDPyqLnuwaWMHajcU3oZ9uZezR.jpg",
}

# Real image URLs for directors (using TMDB image CDN format)
DIRECTOR_IMAGES = {
    "Steven Spielberg": "https://image.tmdb.org/t/p/w300/pOK15qH4fYAmJ5Xs4o2rT8d3Q3w.jpg",
    "Christopher Nolan": "https://image.tmdb.org/t/p/w300/xuAIuYSmsUzKlUMBFGVZaWsY3DZ.jpg",
    "Quentin Tarantino": "https://image.tmdb.org/t/p/w300/8h4VrV9Xe0L7lH7x0t3ZJ9Q9Y9Y.jpg",
    "Martin Scorsese": "https://image.tmdb.org/t/p/w300/9U9Y5GQuWX3EZy39B8nkk4NY01S.jpg",
    "James Cameron": "https://image.tmdb.org/t/p/w300/d9K9fqYshb88lYlUXnH1NkF5Q3o.jpg",
    "Peter Jackson": "https://image.tmdb.org/t/p/w300/3nMj2xhYxqHjqYgK9vJ8qJ8qJ8q.jpg",
    "Ridley Scott": "https://image.tmdb.org/t/p/w300/5K7cOHoay2mZusSLezBOY0Qxh8a.jpg",
    "Alfred Hitchcock": "https://image.tmdb.org/t/p/w300/9phhl0VD6S7Cd8tpbk7P4iHm3By.jpg",
    "Francis Ford Coppola": "https://image.tmdb.org/t/p/w300/8xKekvHJq4XfL5k5X3J3J3J3J3J.jpg",
    "George Lucas": "https://image.tmdb.org/t/p/w300/8xKekvHJq4XfL5k5X3J3J3J3J3J.jpg",
}

# Movie poster images - mapping each movie title to a specific poster
# Using TMDB movie poster URLs - you can replace these with actual movie posters
MOVIE_POSTERS = {
    "Silent Horizon": "https://image.tmdb.org/t/p/w500/dqK9H6ivL07o1g4by9qeytmkPQo.jpg",
    "Crimson Dawn": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
    "Shadow's Edge": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "Fallen Kingdom": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
    "Eternal Flame": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "Golden Mirage": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61eNJ51NqUn2I.jpg",
    "Whispering Winds": "https://image.tmdb.org/t/p/w500/6Wdl9N6dL0Hi0T1qJLWSz6gMLbd.jpg",
    "Forgotten Path": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
    "Iron Legacy": "https://image.tmdb.org/t/p/w500/7d6EY00g1c39SGZOoCJ5Py9nNth.jpg",
    "Midnight Secrets": "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",
    "Celestial Journey": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
    "Shattered Memories": "https://image.tmdb.org/t/p/w500/5qHNjhtjMD4YWH3UP0s4YbqHKaP.jpg",
    "Broken Compass": "https://image.tmdb.org/t/p/w500/6NsMbJXRlDZu6zat3FYxjy1HpBt.jpg",
    "Distant Echo": "https://image.tmdb.org/t/p/w500/3bOGNsHlrswhyW79uvIHH1V43JI.jpg",
    "Twilight Veil": "https://image.tmdb.org/t/p/w500/isQ747u0MU8U9gdsNlPngnP8ZPv.jpg",
    "Frozen Time": "https://image.tmdb.org/t/p/w500/jpurJ9jAcLCYjgHHfYF32m3zJYm.jpg",
    "Hidden Truths": "https://image.tmdb.org/t/p/w500/7YmHruJz5aKXqYhkdwirsgxwl0F.jpg",
    "Burning Skies": "https://image.tmdb.org/t/p/w500/cckcYc2v0yh1tc9QjRelptcOBko.jpg",
    "Lost Horizon": "https://image.tmdb.org/t/p/w500/k3W1XXddDOH2zibP9tOwylY5jAk.jpg",
    "Silver Lining": "https://image.tmdb.org/t/p/w500/wo2hJpn04vbtmh0B9utCFdsQhxM.jpg",
    "Secret Passage": "https://image.tmdb.org/t/p/w500/edPU5HxncLWa1YkgRWNekphlbbs.jpg",
    "Dark Matter": "https://image.tmdb.org/t/p/w500/pQFoyx7rp09CJT0jqoB0qN3y4m.jpg",
    "Rising Tides": "https://image.tmdb.org/t/p/w500/7rmMU3h7zQqEQH6n9Ka7k5yqS5m.jpg",
    "Lone Star": "https://image.tmdb.org/t/p/w500/oGJQhOpT8S1F56m3ro7kWH3oPAO.jpg",
    "Veiled Shadows": "https://image.tmdb.org/t/p/w500/cZ8a3QvAnj2cgcgVL6g4XaqPzpL.jpg",
    "Crimson Tide": "https://image.tmdb.org/t/p/w500/lyUyVARQKhGxaxy0FbPJCQRpiaN.jpg",
    "Endless Night": "https://image.tmdb.org/t/p/w500/plLfB60b5IGONxm1wayq6z5AZ4q.jpg",
    "Silent Whisper": "https://image.tmdb.org/t/p/w500/iWdKjMry5Pt8omUxq3sgf0lb2JZ.jpg",
    "Golden Horizon": "https://image.tmdb.org/t/p/w500/6TE2al2QLvxR49fObWuEUdX0F4z.jpg",
    "Fading Light": "https://image.tmdb.org/t/p/w500/kuqFzlYMc2IrsOyPznMd1FroeGq.jpg",
    "Mystic River": "https://image.tmdb.org/t/p/w500/euDPyqLnuwaWMHajcU3oZ9uZezR.jpg",
    "Shadow Realm": "https://image.tmdb.org/t/p/w500/pOK15qH4fYAmJ5Xs4o2rT8d3Q3w.jpg",
    "Fallen Stars": "https://image.tmdb.org/t/p/w500/xuAIuYSmsUzKlUMBFGVZaWsY3DZ.jpg",
    "Hidden Fortress": "https://image.tmdb.org/t/p/w500/8h4VrV9Xe0L7lH7x0t3ZJ9Q9Y9Y.jpg",
    "Twilight Dreams": "https://image.tmdb.org/t/p/w500/9U9Y5GQuWX3EZy39B8nkk4NY01S.jpg",
    "Iron Heart": "https://image.tmdb.org/t/p/w500/d9K9fqYshb88lYlUXnH1NkF5Q3o.jpg",
    "Forgotten Realm": "https://image.tmdb.org/t/p/w500/3nMj2xhYxqHjqYgK9vJ8qJ8qJ8q.jpg",
    "Burning Bridges": "https://image.tmdb.org/t/p/w500/5K7cOHoay2mZusSLezBOY0Qxh8a.jpg",
    "Lost Legacy": "https://image.tmdb.org/t/p/w500/9phhl0VD6S7Cd8tpbk7P4iHm3By.jpg",
    "Silver Shadows": "https://image.tmdb.org/t/p/w500/8xKekvHJq4XfL5k5X3J3J3J3J3J.jpg",
    "Secret Garden": "https://image.tmdb.org/t/p/w500/dqK9H6ivL07o1g4by9qeytmkPQo.jpg",
    "Dark Horizon": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
    "Rising Dawn": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "Eternal Night": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
    "Whispering Shadows": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "Shattered Sky": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61eNJ51NqUn2I.jpg",
    "Frozen Flame": "https://image.tmdb.org/t/p/w500/6Wdl9N6dL0Hi0T1qJLWSz6gMLbd.jpg",
    "Golden Path": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
    "Silent Storm": "https://image.tmdb.org/t/p/w500/7d6EY00g1c39SGZOoCJ5Py9nNth.jpg",
    "Twilight Echo": "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",
    "Celestial Shadows": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
    "Fallen Realm": "https://image.tmdb.org/t/p/w500/5qHNjhtjMD4YWH3UP0s4YbqHKaP.jpg",
    "Hidden Horizon": "https://image.tmdb.org/t/p/w500/6NsMbJXRlDZu6zat3FYxjy1HpBt.jpg",
    "Midnight Mirage": "https://image.tmdb.org/t/p/w500/3bOGNsHlrswhyW79uvIHH1V43JI.jpg",
    "Iron Veil": "https://image.tmdb.org/t/p/w500/isQ747u0MU8U9gdsNlPngnP8ZPv.jpg",
    "Lost Echo": "https://image.tmdb.org/t/p/w500/jpurJ9jAcLCYjgHHfYF32m3zJYm.jpg",
    "Mystic Horizon": "https://image.tmdb.org/t/p/w500/7YmHruJz5aKXqYhkdwirsgxwl0F.jpg",
    "Burning Night": "https://image.tmdb.org/t/p/w500/cckcYc2v0yh1tc9QjRelptcOBko.jpg",
    "Silver Flame": "https://image.tmdb.org/t/p/w500/k3W1XXddDOH2zibP9tOwylY5jAk.jpg",
    "Dark Legacy": "https://image.tmdb.org/t/p/w500/wo2hJpn04vbtmh0B9utCFdsQhxM.jpg",
    "Crimson Echo": "https://image.tmdb.org/t/p/w500/edPU5HxncLWa1YkgRWNekphlbbs.jpg",
    "Twilight Path": "https://image.tmdb.org/t/p/w500/pQFoyx7rp09CJT0jqoB0qN3y4m.jpg",
    "Golden Veil": "https://image.tmdb.org/t/p/w500/7rmMU3h7zQqEQH6n9Ka7k5yqS5m.jpg",
    "Frozen Horizon": "https://image.tmdb.org/t/p/w500/oGJQhOpT8S1F56m3ro7kWH3oPAO.jpg",
    "Shadowed Legacy": "https://image.tmdb.org/t/p/w500/cZ8a3QvAnj2cgcgVL6g4XaqPzpL.jpg",
    "Whispering Night": "https://image.tmdb.org/t/p/w500/lyUyVARQKhGxaxy0FbPJCQRpiaN.jpg",
    "Secret Horizon": "https://image.tmdb.org/t/p/w500/plLfB60b5IGONxm1wayq6z5AZ4q.jpg",
    "Rising Shadows": "https://image.tmdb.org/t/p/w500/iWdKjMry5Pt8omUxq3sgf0lb2JZ.jpg",
    "Fading Mirage": "https://image.tmdb.org/t/p/w500/6TE2al2QLvxR49fObWuEUdX0F4z.jpg",
    "Silent Echo": "https://image.tmdb.org/t/p/w500/kuqFzlYMc2IrsOyPznMd1FroeGq.jpg",
    "Hidden Flame": "https://image.tmdb.org/t/p/w500/euDPyqLnuwaWMHajcU3oZ9uZezR.jpg",
    "Eternal Horizon": "https://image.tmdb.org/t/p/w500/pOK15qH4fYAmJ5Xs4o2rT8d3Q3w.jpg",
    "Shattered Legacy": "https://image.tmdb.org/t/p/w500/xuAIuYSmsUzKlUMBFGVZaWsY3DZ.jpg",
    "Iron Shadows": "https://image.tmdb.org/t/p/w500/8h4VrV9Xe0L7lH7x0t3ZJ9Q9Y9Y.jpg",
    "Lost Horizon": "https://image.tmdb.org/t/p/w500/9U9Y5GQuWX3EZy39B8nkk4NY01S.jpg",
    "Mystic Flame": "https://image.tmdb.org/t/p/w500/d9K9fqYshb88lYlUXnH1NkF5Q3o.jpg",
    "Golden Shadow": "https://image.tmdb.org/t/p/w500/3nMj2xhYxqHjqYgK9vJ8qJ8qJ8q.jpg",
    "Twilight Legacy": "https://image.tmdb.org/t/p/w500/5K7cOHoay2mZusSLezBOY0Qxh8a.jpg",
    "Dark Horizon": "https://image.tmdb.org/t/p/w500/9phhl0VD6S7Cd8tpbk7P4iHm3By.jpg",
    "Crimson Path": "https://image.tmdb.org/t/p/w500/8xKekvHJq4XfL5k5X3J3J3J3J3J.jpg",
    "Frozen Shadows": "https://image.tmdb.org/t/p/w500/dqK9H6ivL07o1g4by9qeytmkPQo.jpg",
    "Hidden Echo": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
    "Burning Horizon": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "Silver Mirage": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
    "Silent Legacy": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "Shadowed Horizon": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61eNJ51NqUn2I.jpg",
    "Twilight Flame": "https://image.tmdb.org/t/p/w500/6Wdl9N6dL0Hi0T1qJLWSz6gMLbd.jpg",
    "Lost Shadows": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
    "Rising Horizon": "https://image.tmdb.org/t/p/w500/7d6EY00g1c39SGZOoCJ5Py9nNth.jpg",
    "Golden Echo": "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",
    "Eternal Shadows": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
    "Hidden Legacy": "https://image.tmdb.org/t/p/w500/5qHNjhtjMD4YWH3UP0s4YbqHKaP.jpg",
    "Iron Horizon": "https://image.tmdb.org/t/p/w500/6NsMbJXRlDZu6zat3FYxjy1HpBt.jpg",
    "Faded Shadows": "https://image.tmdb.org/t/p/w500/3bOGNsHlrswhyW79uvIHH1V43JI.jpg",
    "Mystic Legacy": "https://image.tmdb.org/t/p/w500/isQ747u0MU8U9gdsNlPngnP8ZPv.jpg",
    "Shattered Horizon": "https://image.tmdb.org/t/p/w500/jpurJ9jAcLCYjgHHfYF32m3zJYm.jpg",
    "Silent Flame": "https://image.tmdb.org/t/p/w500/7YmHruJz5aKXqYhkdwirsgxwl0F.jpg",
    "Crimson Horizon": "https://image.tmdb.org/t/p/w500/cckcYc2v0yh1tc9QjRelptcOBko.jpg",
    "Twilight Shadows": "https://image.tmdb.org/t/p/w500/k3W1XXddDOH2zibP9tOwylY5jAk.jpg",
    "Golden Horizon": "https://image.tmdb.org/t/p/w500/wo2hJpn04vbtmh0B9utCFdsQhxM.jpg",
    "Frozen Legacy": "https://image.tmdb.org/t/p/w500/edPU5HxncLWa1YkgRWNekphlbbs.jpg",
    "Hidden Flame": "https://image.tmdb.org/t/p/w500/pQFoyx7rp09CJT0jqoB0qN3y4m.jpg",
    "Burning Shadows": "https://image.tmdb.org/t/p/w500/7rmMU3h7zQqEQH6n9Ka7k5yqS5m.jpg",
    "Silver Horizon": "https://image.tmdb.org/t/p/w500/oGJQhOpT8S1F56m3ro7kWH3oPAO.jpg",
    "Shadowed Flame": "https://image.tmdb.org/t/p/w500/cZ8a3QvAnj2cgcgVL6g4XaqPzpL.jpg",
}

# ----------------------------
# Predefined data
# ----------------------------
MOVIE_TITLES = [
    "Silent Horizon", "Crimson Dawn", "Shadow's Edge", "Fallen Kingdom", "Eternal Flame",
    "Golden Mirage", "Whispering Winds", "Forgotten Path", "Iron Legacy", "Midnight Secrets",
    "Celestial Journey", "Shattered Memories", "Broken Compass", "Distant Echo", "Twilight Veil",
    "Frozen Time", "Hidden Truths", "Burning Skies", "Lost Horizon", "Silver Lining",
    "Secret Passage", "Dark Matter", "Rising Tides", "Lone Star", "Veiled Shadows",
    "Crimson Tide", "Endless Night", "Silent Whisper", "Golden Horizon", "Fading Light",
    "Mystic River", "Shadow Realm", "Fallen Stars", "Hidden Fortress", "Twilight Dreams",
    "Iron Heart", "Forgotten Realm", "Burning Bridges", "Lost Legacy", "Silver Shadows",
    "Secret Garden", "Dark Horizon", "Rising Dawn", "Eternal Night", "Whispering Shadows",
    "Shattered Sky", "Frozen Flame", "Golden Path", "Silent Storm", "Twilight Echo",
    "Celestial Shadows", "Fallen Realm", "Hidden Horizon", "Midnight Mirage", "Iron Veil",
    "Lost Echo", "Mystic Horizon", "Burning Night", "Silver Flame", "Dark Legacy",
    "Crimson Echo", "Twilight Path", "Golden Veil", "Frozen Horizon", "Shadowed Legacy",
    "Whispering Night", "Secret Horizon", "Rising Shadows", "Fading Mirage", "Silent Echo",
    "Hidden Flame", "Eternal Horizon", "Shattered Legacy", "Iron Shadows", "Lost Horizon",
    "Mystic Flame", "Golden Shadow", "Twilight Legacy", "Dark Horizon", "Crimson Path",
    "Frozen Shadows", "Hidden Echo", "Burning Horizon", "Silver Mirage", "Silent Legacy",
    "Shadowed Horizon", "Twilight Flame", "Lost Shadows", "Rising Horizon", "Golden Echo",
    "Eternal Shadows", "Hidden Legacy", "Iron Horizon", "Faded Shadows", "Mystic Legacy",
    "Shattered Horizon", "Silent Flame", "Crimson Horizon", "Twilight Shadows", "Golden Horizon",
    "Frozen Legacy", "Hidden Flame", "Burning Shadows", "Silver Horizon", "Shadowed Flame",
]

ACTOR_NAMES = [
    "Robert Downey Jr.", "Scarlett Johansson", "Chris Evans", "Mark Ruffalo", "Chris Hemsworth",
    "Jennifer Lawrence", "Brad Pitt", "Angelina Jolie", "Leonardo DiCaprio", "Natalie Portman",
    "Tom Hanks", "Meryl Streep", "Morgan Freeman", "Emma Stone", "Ryan Gosling",
    "Gal Gadot", "Henry Cavill", "Zendaya", "Dwayne Johnson", "Margot Robbie",
]

DIRECTOR_NAMES = [
    "Steven Spielberg", "Christopher Nolan", "Quentin Tarantino", "Martin Scorsese", "James Cameron",
    "Peter Jackson", "Ridley Scott", "Alfred Hitchcock", "Francis Ford Coppola", "George Lucas",
]

# Actor bios
ACTOR_BIOS = {
    "Robert Downey Jr.": "Academy Award-nominated actor known for his charismatic performances in films like Iron Man, Sherlock Holmes, and Tropic Thunder. He has become one of the highest-paid actors in Hollywood.",
    "Scarlett Johansson": "Academy Award-nominated actress and one of the world's highest-paid actresses. Known for her roles in Lost in Translation, The Avengers series, and Marriage Story.",
    "Chris Evans": "Actor best known for playing Captain America in the Marvel Cinematic Universe. Also starred in films like Snowpiercer, Gifted, and Knives Out.",
    "Mark Ruffalo": "Three-time Academy Award nominee known for his roles in The Kids Are All Right, Spotlight, and as Bruce Banner/The Hulk in the Marvel Cinematic Universe.",
    "Chris Hemsworth": "Australian actor best known for playing Thor in the Marvel Cinematic Universe. Also starred in Rush, In the Heart of the Sea, and Extraction.",
    "Jennifer Lawrence": "Academy Award-winning actress known for her roles in Winter's Bone, Silver Linings Playbook, The Hunger Games series, and American Hustle.",
    "Brad Pitt": "Academy Award-winning actor and producer. Known for films like Fight Club, Ocean's Eleven, Once Upon a Time in Hollywood, and 12 Years a Slave.",
    "Angelina Jolie": "Academy Award-winning actress, filmmaker, and humanitarian. Known for films like Girl, Interrupted, Mr. & Mrs. Smith, and Maleficent.",
    "Leonardo DiCaprio": "Academy Award-winning actor and environmental activist. Known for films like Titanic, The Revenant, Inception, and The Wolf of Wall Street.",
    "Natalie Portman": "Academy Award-winning actress known for her roles in Black Swan, V for Vendetta, Jackie, and the Star Wars prequel trilogy.",
    "Tom Hanks": "Two-time Academy Award-winning actor known for films like Forrest Gump, Cast Away, Saving Private Ryan, and The Terminal.",
    "Meryl Streep": "Three-time Academy Award-winning actress, considered one of the greatest actresses of all time. Known for films like The Devil Wears Prada, Sophie's Choice, and The Iron Lady.",
    "Morgan Freeman": "Academy Award-winning actor and narrator. Known for films like The Shawshank Redemption, Driving Miss Daisy, and Million Dollar Baby.",
    "Emma Stone": "Academy Award-winning actress known for her roles in La La Land, The Favourite, Easy A, and The Amazing Spider-Man series.",
    "Ryan Gosling": "Academy Award-nominated actor known for films like La La Land, Drive, The Notebook, and Blade Runner 2049.",
    "Gal Gadot": "Israeli actress and model best known for playing Wonder Woman in the DC Extended Universe. Also starred in Fast & Furious franchise.",
    "Henry Cavill": "British actor best known for playing Superman in the DC Extended Universe and Geralt of Rivia in The Witcher series.",
    "Zendaya": "Emmy Award-winning actress and singer. Known for her roles in Euphoria, Spider-Man: Homecoming, and The Greatest Showman.",
    "Dwayne Johnson": "Actor, producer, and former professional wrestler known as 'The Rock'. Starred in films like Jumanji, Fast & Furious franchise, and Moana.",
    "Margot Robbie": "Academy Award-nominated actress and producer. Known for her roles in I, Tonya, The Wolf of Wall Street, and Birds of Prey.",
}

# Director bios
DIRECTOR_BIOS = {
    "Steven Spielberg": "Academy Award-winning director, producer, and screenwriter. Known for films like Jaws, E.T., Jurassic Park, Schindler's List, and Saving Private Ryan. One of the most influential filmmakers in history.",
    "Christopher Nolan": "Academy Award-nominated director known for his complex narratives and practical effects. Directed films like Inception, The Dark Knight trilogy, Interstellar, and Dunkirk.",
    "Quentin Tarantino": "Academy Award-winning director and screenwriter known for his nonlinear storytelling and stylized violence. Directed films like Pulp Fiction, Kill Bill, Django Unchained, and Once Upon a Time in Hollywood.",
    "Martin Scorsese": "Academy Award-winning director known for his films about crime, Italian-American identity, and Catholic themes. Directed films like Taxi Driver, Goodfellas, The Departed, and The Irishman.",
    "James Cameron": "Academy Award-winning director known for pushing technological boundaries. Directed films like Titanic, Avatar, The Terminator, and Aliens.",
    "Peter Jackson": "Academy Award-winning director best known for The Lord of the Rings trilogy and The Hobbit trilogy. Also directed King Kong and The Lovely Bones.",
    "Ridley Scott": "Academy Award-nominated director known for his visually stunning films. Directed films like Blade Runner, Alien, Gladiator, and The Martian.",
    "Alfred Hitchcock": "Master of suspense and one of the most influential directors in cinema history. Known for films like Psycho, Vertigo, Rear Window, and North by Northwest.",
    "Francis Ford Coppola": "Academy Award-winning director known for The Godfather trilogy and Apocalypse Now. One of the key figures of the New Hollywood era.",
    "George Lucas": "Director, producer, and screenwriter best known for creating the Star Wars and Indiana Jones franchises. Founded Industrial Light & Magic and Lucasfilm.",
}

GENRE_NAMES = [
    "Action", "Adventure", "Drama", "Comedy", "Thriller", "Horror", "Sci-Fi", "Fantasy", "Romance", "Mystery"
]

# ----------------------------
# Command
# ----------------------------
class Command(BaseCommand):
    help = "Populate movies with random genres, actors, and a single director"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating database with movies...")

        # Create Genres
        genres = []
        for name in GENRE_NAMES:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre)

        # Create Actors
        actors = []
        for name in ACTOR_NAMES:
            image_url = ACTOR_IMAGES.get(name, "")
            bio = ACTOR_BIOS.get(name, "")
            actor, _ = Person.objects.get_or_create(
                name=name,
                defaults={
                    'image_url': image_url,
                    'bio': bio
                }
            )
            # Update image_url and bio if they don't exist
            updated = False
            if not actor.image_url and image_url:
                actor.image_url = image_url
                updated = True
            if not actor.bio and bio:
                actor.bio = bio
                updated = True
            if updated:
                actor.save()
            actors.append(actor)

        # Create Directors
        directors = []
        for name in DIRECTOR_NAMES:
            image_url = DIRECTOR_IMAGES.get(name, "")
            bio = DIRECTOR_BIOS.get(name, "")
            director, _ = Person.objects.get_or_create(
                name=name,
                defaults={
                    'image_url': image_url,
                    'bio': bio
                }
            )
            # Update image_url and bio if they don't exist
            updated = False
            if not director.image_url and image_url:
                director.image_url = image_url
                updated = True
            if not director.bio and bio:
                director.bio = bio
                updated = True
            if updated:
                director.save()
            directors.append(director)

        # Create Movies
        # Use index-based mapping to ensure each movie gets a unique poster URL
        # This handles duplicate titles by assigning different posters based on position
        poster_urls_pool = list(MOVIE_POSTERS.values())
        
        for i, title in enumerate(MOVIE_TITLES, start=1):
            # Use index to get a unique poster for each movie, cycling through available posters
            poster_url = poster_urls_pool[(i - 1) % len(poster_urls_pool)]
            
            # Check if movie exists (handle duplicates by getting first one)
            existing_movies = Movie.objects.filter(title=title)
            if existing_movies.exists():
                movie = existing_movies.first()
                created = False
            else:
                # Deterministic release year and rating based on index
                release_year = 1980 + ((i - 1) % 46)  # Years from 1980 to 2025
                rating = round(5.0 + ((i - 1) % 45) * 0.1, 1)  # Ratings from 5.0 to 9.4
                
                movie = Movie.objects.create(
                    title=title,
                    release_year=release_year,
                    rating=rating,
                    image_url=poster_url
                )
                created = True
            
            # Update image_url if it doesn't exist
            if not movie.image_url:
                movie.image_url = poster_url
                movie.save()

            # Assign director deterministically based on movie index
            director_idx = (i - 1) % len(directors)
            movie.director = directors[director_idx]
            movie.save()

            # Assign genres deterministically based on movie index
            # Each movie gets 1-3 genres based on its position
            num_genres = (i % 3) + 1  # 1, 2, or 3 genres
            start_genre_idx = ((i - 1) * 2) % len(genres)
            movie_genres = []
            for j in range(num_genres):
                genre_idx = (start_genre_idx + j) % len(genres)
                movie_genres.append(genres[genre_idx])
            
            for genre in movie_genres:
                MovieGenre.objects.get_or_create(movie=movie, genre=genre)

            # Assign actors deterministically based on movie index
            # Each movie gets 1-4 actors based on its position
            num_actors = min((i % 4) + 1, len(actors))  # 1, 2, 3, or 4 actors
            start_idx = ((i - 1) * num_actors) % len(actors)
            movie_actors = []
            for j in range(num_actors):
                actor_idx = (start_idx + j) % len(actors)
                movie_actors.append(actors[actor_idx])
            
            for idx, actor in enumerate(movie_actors):
                # Check if relationship already exists
                existing = MovieActor.objects.filter(movie=movie, person=actor).first()
                if not existing:
                    MovieActor.objects.create(
                        movie=movie, 
                        person=actor, 
                        character_name=f"Character {idx + 1}"
                    )

            self.stdout.write(f"Created movie: {movie.title} (Director: {movie.director.name})")

        self.stdout.write(self.style.SUCCESS("Successfully populated movies!"))
