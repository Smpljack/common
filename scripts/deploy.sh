#!/bin/bash
export SCRIPTDIR=`dirname $0`
export BASEDIR="${SCRIPTDIR}/.."
export GENERATORDIR="${BASEDIR}/page_generator"
export OUTPUTDIR="${BASEDIR}/docs/generated"

echo "generating pages..."
${GENERATORDIR}/generate.sh
echo "showing changes..."
git diff "${OUTPUTDIR}"
echo "deploying..."
git add "${OUTPUTDIR}"
${SCRIPTDIR}/commit.sh
${SCRIPTDIR}/travis_push.sh
