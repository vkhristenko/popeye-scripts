#!/bin/bash

sbatch --reservation=maint-ticket_2577 submit_cmsRun_cn.sh
sbatch --reservation=maint-ticket_2577 submit_cmsRun_dam.sh
sbatch --reservation=maint-ticket_2577 submit_cmsRun_esb.sh
