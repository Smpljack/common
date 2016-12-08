#!/bin/bash
export SCRIPTDIR=`dirname $0`
export BASEDIR="${SCRIPTDIR}/.."
export GENERATORDIR="${BASEDIR}/page_generator"
export OUTPUTDIR="${BASEDIR}/docs/generated"

${GENERATORDIR}/generate.sh
git add "${OUTPUTDIR}"
${SCRIPTDIR}/commit.sh
${SCRIPTDIR}/travis_push.sh
