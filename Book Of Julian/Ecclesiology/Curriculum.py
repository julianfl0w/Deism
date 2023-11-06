{
    "Observe": {  # Input observations of hard reality
        "Divine": {
            "meta": dict(required=1),
            "Physics": {},  # Emergence downward. Physics is the basis
            "Chem": {},  # From which arise chem and astro
            "Astro": {},
        },
        "Human": {
            "meta": dict(required=2),
            "Body": {
                "Bio": {
                    "Stats": {},
                    "Chem": {},
                },
                "DNA": {
                    "Epigenetics": {},
                    "Cellular Expression": {},
                    "Genomics": {},
                },
                "Hormone": {},
            },
            "Mind": {
                "Linguistics": {},
                "Psych": {},
                "Society": {
                    "Computationally": {},
                },
                "Religion": {},
                "Government": {},
                "Histoy": {
                    "China": {},
                },
            },
        },
    },
    "Design": {  # Output design for human
        "Human": {
            "Body": {
                "meta": dict(required=1),
                "Vision": {},
                "Senses": {},
                "Locomotion": {},
                "Comms": {
                    "Wired": {},
                    "Wireless": {},
                    "Signals": {},
                    "Secure": {
                        "Encryption": {},
                        "Blockchain": {},
                        "Network": {},
                    },
                },
            },
            "Mind": {
                "meta": dict(required=1),
                "Ops": {
                    "Scrum Practitioner": {},
                    "Project Management": {},
                },
                "Computer":{
                    "Cybernet": {},
                    "Deep NN": {},
                    "Linear Algebra in GPU": {},
                },
                # "Differential Equations": {}, dubious value
                "Comms": {
                    "meta": dict(required=2),
                    "Graphic": {
                        "Web": {"A Course in HTML/CSS/JS": {}},
                        "Android": {},
                        "Game": {
                            "Unity": {},
                        },
                    },
                    "Cloud Cert": {
                        "meta": {"required": 1},
                        "AWS Cloud Practitioner": {},
                        "AWS Cloud Quest": {},
                        "GCP Practitioner": {},
                        "Azure Practitioer": {},
                    },
                },
            },
        },
    },
    "Maintain": {
        "meta": dict(required=2),
        "Human": {
            "Mind": {
                "Therapy": {"Psyc": {}},
                "Cognitive Behavioral": {},
                "Book Of Julian": {"meta": dict(required=1)},
            },
            "Body": {
                "Pharma": {},
                "Imaging": {},
                "Genes": {},
                "Blood": {},
            },
        },
    },
}
