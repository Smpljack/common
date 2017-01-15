#!/bin/bash
SCRIPTDIR=`dirname $0`
export SCRIPTDIR=`realpath ${SCRIPTDIR}`
export BASEDIR="${SCRIPTDIR}/.."
export GENERATORDIR="${BASEDIR}/page_generator"
export OUTPUTDIR="${BASEDIR}/docs/generated"
export PYTHONPATH="${BASEDIR}/python:${PYTHONPATH}"

git checkout master
echo "generating pages..."
pushd .
cd ${GENERATORDIR}
./generate.sh
popd
echo "showing changes..."
git diff "${OUTPUTDIR}"
echo "deploying..."
git add "${OUTPUTDIR}"
${SCRIPTDIR}/commit.sh
${SCRIPTDIR}/travis_push.sh
