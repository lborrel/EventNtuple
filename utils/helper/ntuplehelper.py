import os

class nthelper:

    single_object_branches = ['evtinfo', 'evtinfomc', 'hitcount', 'tcnt', 'crvsummary', 'crvsummarymc']
    vector_object_branches = ['trk', 'trkmc', 'trkcalohit', 'trkcalohitmc', 'crvcoincs', 'crvcoincsmc', 'crvcoincsmcplane', 'trkqual']
    vector_vector_object_branches = ['trksegs', 'trksegpars_lh', 'trksegpars_ch', 'trksegpars_kl', 'trkmcsim', 'trkhits', 'trkhitsmc', 'trkmats', 'trkmcsci', 'trkmcssi', 'trksegsmc' ]

    track_types_dict = { 'kl' : "kinematic line fit (i.e. straight-line fit)",
                         'dem' : "downstream e-minus fit",
                         'uem' : "upstream e-minus fit",
                         'dmm' : "downstream mu-minus fit",
                         'umm' : "upstream mu-minus fit",
                         'dep' : "downstream e-plus fit",
                         'uep' : "upstream e-plus fit",
                         'dmp' : "downstream mu-plus fit",
                         'ump' : "upstream mu-plus fit"
                        }

    # A dictionary of branch name to header file containing the struct
    branch_struct_dict = { 'evtinfo' : "EventInfo",
                           'evtinfomc' : "EventInfoMC",
                           'hitcount' : "HitCount",
                           'tcnt' : "TrkCount", # TODO: leaves can't be retrieved because they are runtime made
                           'trk' : "TrkInfo",
                           'trksegs' : "TrkSegInfo",
                           'trkmc' : "TrkInfoMC",
                           'trksegpars_lh' : "LoopHelixInfo",
                           'trksegpars_ch' : "CentralHelixInfo",
                           'trksegpars_kl' : "KinematicLineInfo",
                           'trkmcsim' : "SimInfo",
                           'trkcalohit' : "TrkCaloHitInfo",
                           'trkcalohitmc' : "CaloClusterInfoMC",
                           'trkhits' : "TrkStrawHitInfo",
                           'trkhitsmc' : "TrkStrawHitInfoMC",
                           'trkmats' : "TrkStrawMatInfo",
                           'trkmcsci' : "MCStepInfo",
                           'trkmcssi' : "MCStepSummaryInfo",
                           "crvsummary" : "CrvSummaryReco",
                           "crvsummarymc" : "CrvSummaryMC",
                           "crvcoincs" : "CrvHitInfoReco",
                           "crvcoincsmc" : "CrvHitInfoMC",
                           "crvcoincsmcplane" : "CrvPlaneInfoMC",
                           "trkqual" : "MVAResultInfo",
                           "helices" : "HelixInfo",
                           "trksegsmc" : "SurfaceStepInfo"
                          }

    #
    def get_branch_explanation(self, branch):
        explanation=""
        if branch in self.track_types_dict.keys():
            explanation = "This is an outdated (v5) branch."
        else:
            explanation = branch + ": ";
            struct = self.branch_struct_dict[branch]
            struct_file = struct + ".hh";
            with open(os.environ.get("EVENTNTUPLE_INC")+"/EventNtuple/inc/"+struct_file, 'r') as f:
                lines = f.readlines()
                for row in lines:
                    if (row.find("// "+struct) != -1):
                        explanation += row.replace("// "+struct+":", "").replace('\n', ''); # remove the trailing newline as well

        return explanation

    def list_all_branches(self):
        print("Single-Object Branches")
        print("======================")
        for branch in self.single_object_branches:
            print(self.get_branch_explanation(branch))
        print("\nVector Branches")
        print("================")
        for branch in self.vector_object_branches:
            print(self.get_branch_explanation(branch))
        print("\nVector-of-Vector Branches")
        print("=============================")
        for branch in self.vector_vector_object_branches:
            print(""+self.get_branch_explanation(branch))

    # def check_track_type(self, branch):
    #     retval = ["", ""]
    #     if "crv" not in branch: # "umm" is matching "crvsummary"
    #         for key in self.track_types_dict:
    #             if key in branch: # branch could be "demmc" but key will be "dem"
    #                 retval = [key, self.track_types_dict[key]]
    #                 break

    #     return retval

    def whatis(self, array):
        if type(array) is not list: # if a single string is passed, put it into an array
            array = [array]

        # Let's collect leaves from the same branch so that we don't repeat information
        branch_leaves_dict = {}
        for item in array:
            # Expecting "item" to be of form "branch.leaf"
            tokens = item.split('.')
            branch = tokens[0]
            leaf = ""
            if len(tokens)>1:
                leaf = tokens[1]
            try:
                branch_leaves_dict[branch].append(leaf)
            except KeyError:
                branch_leaves_dict[branch] = [leaf]

        for i_branch, leaves in branch_leaves_dict.items():
#            print(i_branch, leaves)

            # Check if this is a track branch
            branch_explanation = self.get_branch_explanation(i_branch)
            branch_to_search = i_branch
            track_type, explanation = self.check_track_type(i_branch)
            branch_output = i_branch + " branch: ";
            if (explanation != ""):
                branch_to_search = i_branch.replace(track_type, "trk", 1) # we have keyed all the different track-related branches to "trk" in e.g. branch_struct_dict; also only replace 1 occurance so that klkl branch is handled correctly

            leaf_output = "";
            leaf_explanations = {};
            try:
                struct = self.branch_struct_dict[branch_to_search]
                struct_file = struct;
                if (".hh" not in struct_file):
                    struct_file += ".hh"



#                print(struct_file)
                with open(os.environ.get("EVENTNTUPLE_INC")+"/EventNtuple/inc/"+struct_file, 'r') as f:
                    lines = f.readlines()
                    for row in lines:
                        if (row.find("// "+struct) != -1):
                            #print(row)
                            branch_output += row.replace("// "+struct+":", "").replace('\n', ''); # remove the trailing newline as well
                            if (i_branch in self.single_object_branches):
                                branch_output += ".\n   - structure: single object"
                                branch_output += "\n   - object: "+struct
                            elif (i_branch in self.vector_object_branches):
                                branch_output += ".\n   - structure: vector of objects"
                                branch_output += "\n   - object: "+ struct
                                branch_output += "\n   - example: ["+i_branch+"1, "+i_branch+"2, ..., "+i_branch+"N]"
                            elif (i_branch in self.vector_vector_object_branches):
                                branch_output += ".\n   - structure: vector of vector of objects"
                                branch_output += "\n   - object: "+ struct
                                # split branch name into "trk" + other thing, and remove the trailing 's' indicating it is plural
                                split_on="trk"
                                token=i_branch.split(split_on)[1].rstrip('s')
                                branch_output += "\n   - example: [ ["+split_on+"1_"+token+"A, "+split_on+"1_"+token+"B, ... ], [ "+split_on+"2_"+token+"A, "+split_on+"2_"+token+"C, ... ], ..., ["+split_on+"N_"+token+"B, "+split_on+"N_"+token+"D, ... ] ]"
                        # Check whether this row is an explanation for a leaf that we are asking for
                        for i_leaf in leaves:
                            if i_leaf == "*":
                                if (row.find(" = ") != -1) and (row.find(";") != -1) and (row.find("//") != -1):
                                    if i_leaf not in leaf_explanations: # we want to only take the first occurance
                                        leaf_explanations[i_leaf] = "\n"+row
                                    else:
                                        leaf_explanations[i_leaf] += row;
                            else:
                                if (row.find(" "+i_leaf+" ") != -1) or (row.find(" "+i_leaf+";") != -1): # add spaces around leaf so that we don't find substrings
                                    if i_leaf not in leaf_explanations: # we want to only take the first occurance
                                        leaf_explanations[i_leaf] = row
            except KeyError:
                print(branch_to_search+" is not in branch_struct_dict...\n")

            # Check that we have all the explanations...
            for i_leaf in leaves:
                if i_leaf not in leaf_explanations:
                    leaf_explanations[i_leaf] = "not found\n";
                # ... and produce the output text
                leaf_output += i_branch + "." + i_leaf + ": "+leaf_explanations[i_leaf];

            # Display the output text
            print(branch_output)
            print(leaf_output)
