Genesis = {
    "meta": {"priority": -10000},
    "Fourteen billion years ago, God created our universe": {},
    "It started from nothing, then expanded rapidly": {},
    "And the earth was without form": {},
    "Five billion years ago, the earth coalesced, in orbit around the sun": {},
    "Shortly thereafter, organized life emerged from the chaos": {},
    "Many generations passed": {},
    "300 thousand years ago, humankind originated in Africa": {},
    "And we expanded throughout the earth": {},
    "At that time, chaos governed our steps": {},
    "But we were united under a common God": {},
    "Now we seek to know God": {},
}

Covenant_Origins = {
    "meta": dict(priority=0),
    "Following covenant theology, our lineage consists of:": {
        "meta": {"type": "list"},
        "The First Testament, a covenant of works requiring animal sacrifice, making no promise of a life after death": {},
        "The Second Testament, a covenant of grace, alluding to a life after death": {},
        "The Third Testament, a covenant of love, making no promise of a life after death": {},
    },
    "Simplified": {
        "meta": {"type": "lineage", "graphParams": {"rankdir": "LR"}},
        "Works": {"Grace": {"Love": {}}},
    },
}

Evolutionary_Origins = {
    "meta": dict(priority=0),
    "The Tree of Life": {},
    "This is our evolutionary lineage:": {},
    "Evolutionary Lineage": {
        "meta": {"type": "list", "topology": "flat"},
        "The Fundamental Particles, which is the soil": {
            "LUCA, which is the seed": {
                "Eukarya, the trunk": {
                    "Animalia, the largest branches": {
                        "Humankind, the leaves": {
                            "The Son of Man, who will usher in the new age": {}
                        }
                    }
                }
            }
        },
    },
}

Ideological_Origins = {
    "meta": dict(priority=0),
    "Introduction":{
        "In the beginning, there was no religion, for there was no language": {},
        "Then there were many gods, for there were no standards": {},
        "This was the beginning of the Spiritual Age": {},
        "Then there was one God, and his name was Jehovah": {},
        "Then there were three Gods in one, the holy trinity": {},
        "Now there is one God, outside of this universe": {},
        "This is the path by which we have entered the Metaphysical Age": {},
        "In the Beatific Vision, when we see the face of God, we will enter the Positive Age": {},
    },
    "Our Ideological Lineage is an evolutionary heritage, delineated by major reformational events": {
        "meta": {"type": "lineage", "name": "Ideological Spiritual Lineage"},
        "Atheism": {
            "Polytheism": {
                "Judaism": {
                    "Christianity": {"Islam": {}, "Protestantism": {"Deism": {}}}
                },
                "Hinduism": {},
            }
        },
    },
    "In the Law of Three Stages, Deism represents the Metaphysical stage": {
        "The Three Stages": {
            "meta": {"type": "lineage", "graphParams": {"rankdir": "LR"}},
            "Spiritual": {"Metaphysical": {"Positive": {}}},
        }
    },
}

Migratory_Origins = {
    "meta":dict(priority=0),
    "This is our migratory history, which is the basis of our racial theory": {
        "meta": {"type": "list", "topology": "flat"},
        "300,000 years ago, humankind originated in Africa": {},
        "150,000 years ago, we expanded into Eurasia": {},
        "50,000 years ago, we expanded into Australia": {},
        "15,000 years ago, we expanded into America": {}
    },
    "Simplified migratory chart": {
        "meta": {"type": "lineage", "name": "Migratory Lineage"},
        "Africa": {"Europe": {}, "Asia": {"America": {}}, "Australia": {}},
    },
    "Based upon the first migration, there are three races: African, Asian, and European": {},
}

Recognized_Theologians = {
    "The Tree of Spirit": {},
    "Deism recognizes the following theologians as a part of our lineage": {},
    "Abraham, who established the first covenant": {},
    "David, who unified the people": {},
    "Jesus, who established the second covenant": {},
    "Paul, who established the church": {},
    "Constantine, who unified the people": {},
    "Thomas Aquinas, who unified the doctrine": {},
    "Martin Luther, who refined the doctrine": {},
    "And finally Julian Coy, who established the third covenant and administers the Deist religion worldwide": {}
}
