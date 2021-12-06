#!/bin/bash

# add the papers number to get the total number of papers


expr `cat num_journals.text` + `cat num_confs_select.text` +  `cat num_confs_select2.text`  + `cat num_confs_other.text` > num_total.text

