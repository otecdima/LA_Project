import librosa
from database import generate_hashes_song, find_peaks_maximum, create_database


def get_matches(hashes, database):
    hashes_dict = {}
    for hash_, time_ in hashes:
        hashes_dict[hash_] = time_

    just_hashes = [str(hash_[0]) for hash_ in hashes]

    matched = {}
    for song, hash_ in database.items():
        for hash_song in hash_:
            if hash_song[0] in just_hashes:
                if song in matched:
                    matched[song].append((hash_song[1], hashes_dict[hash_song[0]]))
                else:
                    matched[song] = [(hash_song[1], hashes_dict[hash_song[0]])]
    if matched == {}:
        return None
    return matched


def best_match(matches):
    matched_song = None
    best_score = 0
    for song, coincides in matches.items():
        if len(coincides) < 2:
            continue
        differences = list(map(lambda x: x[0] - x[1], coincides))
        max_occurrence = differences.count(max(differences, key=differences.count))
        if max_occurrence > best_score:
            best_score = max_occurrence
            matched_song = song
    return matched_song if best_score != 0 else None


def main_main(path):
    sample, sampling_rate = librosa.load(path)
    peaks = find_peaks_maximum(sample, sampling_rate)
    hashes_unknown = generate_hashes_song(peaks)
    database = create_database()
    matches = get_matches(hashes_unknown, database)
    if matches is not None:
        matched_song = best_match(matches)
        if matched_song is not None:
            return matched_song
        else:
            return "No Result :("
    else:
        return "No Result :("
