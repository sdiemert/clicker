/**
 * Created by sdiemert on 15-08-30.
 */

/**
 * Aggreates data by initiative name
 *
 * @param agg {Object} - { initiative_name { tag_name : { time : Number, ... }, ... }, ... }
 * @param obj {Object} - reference to obj to put aggregate in, creates new object if not provided.
 */
function aggregateByInitiative(agg, obj){

    obj = obj || {};

    for(var i in agg){

        obj[i] = 0;

        for(var t in agg[i]){

            for(var ts in agg[i][t]){

                obj[i] += agg[i][t][ts];

            }

        }

    }

    return obj;

}

/**
 * Aggreates data for a single initiative by tag name name
 *
 * @param agg {Object} - { tag_name : { time : Number, ... }, ... }
 * @param obj {Object} - reference to obj to put aggregate in, creates new object if not provided.
 */
function aggregateByTag(agg, obj){

    obj = obj || {};

    for(var i in agg){

        obj[i] = 0;

        for(var t in agg[i]){

            obj[i] += agg[i][t];

        }

    }

    return obj;

}

function getIdFromName(s) {

    s = s.replace(" ", "-");
    s = s.toLowerCase();

    return s;

}

