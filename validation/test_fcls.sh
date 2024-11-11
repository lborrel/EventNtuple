#
# test_fcls.sh - runs fcl files to make sure that they complete successfully
# Note: requires relevant filelists in a directory above this one
#

log_file="test_fcls.log"
rm ${log_file}

mock_dataset="mcs.mu2e.ensembleMDS1aOnSpillTriggered.MDC2020ai_perfect_v1_3.art"
primary_dataset="mcs.mu2e.CeEndpointOnSpillTriggered.MDC2020ae_best_v1_3.art"
mixed_dataset="mcs.mu2e.CeEndpointMix2BBTriggered.MDC2020ae_best_v1_3.art"
extracted_dataset="mcs.mu2e.CosmicCRYExtractedCatTriggered.MDC2020ae_best_v1_3.art"
mock_digi_dataset="dig.mu2e.ensembleMDS1aOnSpillTriggered.MDC2020ai_perfect_v1_3.art"

all_datasets=( $mock_dataset $primary_dataset $mixed_dataset $extracted_dataset $mock_digi_dataset )

if [ ! -d ../filelists ]; then
     echo "Making directory ../filelists/"
     mkdir ../filelists/
fi

for dataset in "${all_datasets[@]}"
do
    if [ ! -f ../filelists/$dataset.list ]; then
        echo "File list for $dataset doesn't exist. Creating..."
        setup dhtools
        samListLocations -d --defname $dataset > ../filelists/$dataset.list
    fi
done


echo -n "from_mcs-mockdata.fcl... "
mu2e -c fcl/from_mcs-mockdata.fcl -S ../filelists/$mock_dataset.list --TFileName nts.ntuple.mock.root -n 100 > ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "from_mcs-mockdata_noMC.fcl... "
mu2e -c fcl/from_mcs-mockdata_noMC.fcl -S ../filelists/mcs.mu2e.ensemble-1BB-CEDIOCRYCosmic-2400000s-p95MeVc-Triggered.MDC2020ae_perfect_v1_3.art.list --TFileName nts.ntuple.mockNoMC.root -n 100 >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "from_mcs-primary.fcl... "
mu2e -c fcl/from_mcs-primary.fcl -S ../filelists/mcs.mu2e.CeEndpointOnSpillTriggered.MDC2020ae_best_v1_3.art.list --TFileName nts.ntuple.primary.root -n 100 >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "from_mcs-mixed.fcl... "
mu2e -c fcl/from_mcs-mixed.fcl -S ../filelists/mcs.mu2e.CeEndpointMix2BBTriggered.MDC2020ae_best_v1_3.art.list --TFileName nts.ntuple.mixed.root -n 100 >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "from_mcs-extracted.fcl... "
mu2e -c fcl/from_mcs-extracted.fcl -S ../filelists/mcs.mu2e.CosmicCRYExtractedCatTriggered.MDC2020ae_best_v1_3.art.list --TFileName nts.ntuple.extracted.root -n 100 >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "from_mcs-ceSimReco.fcl... "
mu2e -c Production/Validation/ceSimReco.fcl -n 10 >> ${log_file} 2>&1
mu2e -c fcl/from_mcs-ceSimReco.fcl -s mcs.owner.val-ceSimReco.dsconf.seq.art --TFileName nts.ntuple.ceSimReco.root >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "from_mcs-mockdata_separateTrkBranches.fcl... "
mu2e -c fcl/from_mcs-mockdata_separateTrkBranches.fcl -S ../filelists/mcs.mu2e.ensemble-1BB-CEDIOCRYCosmic-2400000s-p95MeVc-Triggered.MDC2020ae_perfect_v1_3.art.list --TFileName nts.ntuple.mockSepTrkBranches.root -n 100 >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "from_mcs-mockdata_selectorExample.fcl... "
mu2e -c fcl/from_mcs-mockdata_selectorExample.fcl -S ../filelists/mcs.mu2e.ensemble-1BB-CEDIOCRYCosmic-2400000s-p95MeVc-Triggered.MDC2020ae_perfect_v1_3.art.list --TFileName nts.ntuple.mockSelector.root -n 100 >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "from_dig-mockdata.fcl... "
mu2e -c fcl/from_dig-mockdata.fcl -S ../filelists/dig.mu2e.ensemble-1BB-CEDIOCRYCosmic-2400000s-p95MeVc-Triggered.MDC2020ae_perfect_v1_3.art.list --TFileName nts.ntuple.dig.root -n 100 >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "creating file for validation script... "
mu2e -c fcl/from_mcs-mockdata.fcl -S ../filelists/mcs.mu2e.ensemble-1BB-CEDIOCRYCosmic-2400000s-p95MeVc-Triggered.MDC2020ae_perfect_v1_3.art.list --TFileName nts.ntuple.after.root -n 100 >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi

echo -n "creating validation file... "
root -l -b -q validation/create_val_file.C\(\"nts.ntuple.after.root\",\"val.ntuple.after.root\"\) >> ${log_file} 2>&1
if [ $? == 0 ]; then
    echo "OK"
else
    echo "FAIL"
fi
