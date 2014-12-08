import os
import sys
import json
import random
import ConfigParser

# Config file location, home directory by default
config_file = 'kk-config.cfg'
config_file = os.path.expanduser(config_file)

config = ConfigParser.ConfigParser()
config.readfp(open(config_file))

# Participants json file location
participants_json_file = os.getcwd() + "/" + "participants.json"
print(participants_json_file)

def create_list_of_everyone(json_file):
    couples = return_couples(json_file)
    singles = return_singles(json_file)
    if singles:
        return couples[:] + singles[:]
    else:
        return couples[:]


def return_couples(json_file):
    couples = []
    for couple in json_file["participant_couples"]:
        couples.append(json_file["participant_couples"][couple][0]["name"])
        couples.append(json_file["participant_couples"][couple][1]["name"])
    return couples


def return_singles(json_file):
    try:
        singles = [single["name"] for single in json_file["participants"]]
    except KeyError:
        return None
    return singles


def return_partner(name, json_file):
    partner = None
    for couples in json_file["participant_couples"]:
        if name == json_file["participant_couples"][couples][0]["name"]:
            print("%s partner is %s" % (name, json_file["participant_couples"][couples][1]["name"]))
            return json_file["participant_couples"][couples][1]["name"]
        elif name == json_file["participant_couples"][couples][1]["name"]:
            print("%s partner is %s" % (name, json_file["participant_couples"][couples][0]["name"]))
            return json_file["participant_couples"][couples][0]["name"]
    return partner


def generate_kks(json_file):
    pass


def main():
    kk_dict = {}
    if os.path.exists(participants_json_file):
        with open(participants_json_file, 'r') as participants_json_fp:
            participants_json = json.load(participants_json_fp)
    else:
        print("Error: No participants file found!")

    #print create_list_of_everyone(participants_json)

    #print("Partner of James is: %s" % return_partner("James", participants_json))

    everyone = tuple(create_list_of_everyone(participants_json))

    def selection(givers, receivers, name, partner=None):
        """Removes partner from _list and makes random selection"""
        kk = None
        _receivers = receivers
        print _receivers
        def get_kk():
            if len(_receivers) <= 1:
                try:
                    kk = _receivers[0]
                except IndexError:
                    print("IndexError")
                    kk = None
            else:
                kk = _receivers[random.randrange(0, len(_receivers))]
            return kk
        if partner:
            print("removed: %s" % partner)
            try:
                print _receivers
                if partner in _receivers:
                    print("%s is in list.. shouldn't get ValueError" % partner)
                _receivers.remove(partner)
            except ValueError as e:
                print("Value error")
                print e
                print("%s is not in receivers list: %s" % (name, partner))
                print _receivers
            kk = get_kk()
        else:
            kk = get_kk()
        # Re add partner
        if partner:
            _receivers.append(partner)
            print("added: %s" % partner)
            print(_receivers)
        #while kk in complete:
        #    kk = get_kk()
        return kk, _receivers

    people = list(everyone[:])
    list_of_g = list(everyone[:])
    list_of_r = list(everyone[:])
    def generate(everyone, list_of_r, list_of_g):
        kk = "Error"
        error_status = False
        for person in everyone:
            # Get current persons partner
            print("Should be checking partner for: %s" % person)
            partner = return_partner(person, participants_json)
            print("%s partner is: %s" % (person, partner))
            # If person has a partner remove them from the selection
            if partner:
                kk, list_of_r = selection(list_of_g, list_of_r, person, partner)
                while kk == person:
                    kk, list_of_r = selection(list_of_g, list_of_r, person, partner)
                    if len(list_of_r) == 1 and person == list_of_r[0]:
                        print("error")
                        kk = "Error"
            else:
                kk, list_of_r = selection(list_of_g, list_of_r, person)
                while kk == person:
                    kk, list_of_r = selection(list_of_g, list_of_r, person, partner)
                    if len(list_of_r) == 1 and person == list_of_r[0]:
                        print("error")
                        kk = "Error"
            if kk and not kk == "Error":
                #print kk
                list_of_g.remove(person)
                try:
                    list_of_r.remove(kk)
                except ValueError:
                    print "value error"
                    error_status = True
                    return kk_dict, error_status
                #print list_of_r
                kk_dict[person] = kk
            elif kk == "Error":
                error_status = True
                return kk_dict, error_status
        return kk_dict, error_status
    kk_dict, error_status = generate(everyone, list_of_r, list_of_g)

    if error_status:
        print "Error happened"
        people = list(everyone[:])
        list_of_g = list(everyone[:])
        list_of_r = list(everyone[:])
        kk_dict, error_status = generate(everyone, list_of_r, list_of_g)
    if not error_status:
        for key in kk_dict:
            print("%s %s" % (key, kk_dict[key]))
        #print "give" + str(list_of_g)
        #print "recieve" + str(list_of_r)

    #print(json.dumps(participants_json, indent=2))
    # print "Couples:"
    # for couples in participants_json["participant_couples"]:
    #     print participants_json["participant_couples"][couples][0]["name"], \
    #             participants_json["participant_couples"][couples][1]["name"]
    # print "Singles:"
    # for idx, single in enumerate(participants_json["participants"]):
    #     print participants_json["participants"][idx]["name"]




if __name__ == "__main__":
    main()