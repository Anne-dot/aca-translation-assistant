<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
    <ns uri="urn:iso:std:iso:30042:ed-2" prefix="tbx" />
	<!-- Note - this schema only includes the elements and attributes specific to TBX-Basic. It does not include the 
	elements and attributes inherited from TBX-Core. In order to validate a TBX-Basic document instance, the document instance must include declarations both to this schema and to the schema for TBX-Core -->
    
    <pattern id="adminTypeAttr">
        <rule context="tbx:admin">
            <assert test="@type='customerSubset' or @type='projectSubset' or @type='source'">
                admin @type must take one of the following values: 'customerSubset', 'projectSubset', 'source'
            </assert>
            <report test="@type='customerSubset' and not(parent::tbx:conceptEntry or parent::tbx:termSec)">
                customerSubset must be declared at concept or term levels.
            </report>
            <report test="@type='projectSubset' and not(parent::tbx:conceptEntry or parent::tbx:termSec)">
                projectSubset must be declared at concept or term levels.
            </report>
            <report test="@type='source' and not(parent::tbx:descripGrp[parent::tbx:termSec] or parent::tbx:termSec or parent::tbx:descripGrp[parent::tbx:conceptEntry] or parent::tbx:descripGrp[parent::tbx:langSec])">
                source must be declared 1. At the term level: (a) nested in a descripGrp (to describe the source of context), or (b) non-nested (to refer to the source of the term). 2. At the concept or lang level: nested in a descripGrp (to describe the source of a definition).
            </report>
        </rule>
    </pattern>
    
    <pattern id="descrTypeAttr">
        <rule context="tbx:descrip">
            <assert test="@type='context' or @type='definition' or @type='subjectField'">
                descrip @type must take one of the following values: 'context', 'definition', 'subjectField'
            </assert>
            <report test="(@type='subjectField') and not(parent::tbx:conceptEntry)">
                subjectField must be declared at concept level.
            </report>
            <report test="(@type='context') and not(parent::tbx:termSec or parent::tbx:descripGrp[parent::tbx:termSec])">
                context must be declared at term level, nested in descripGrp with an admin element if accompanied by a source.
            </report>
            <report test="(@type='definition') and not((parent::tbx:conceptEntry|parent::tbx:langSec) or parent::tbx:descripGrp[parent::tbx:conceptEntry|parent::tbx:langSec])">
                definition must be declared at concept or language levels, nested in descripGrp with an admin element if accompanied by a source.
            </report>
        </rule>
    </pattern>
    
    <pattern id="refTypeAttr">
	<!-- what about the target attribute?-->
        <rule context="tbx:ref">
            <assert test="@type='crossReference'">
                ref @type must take the value: 'crossReference'
            </assert>
            <report test="(@type='crossReference') and not(parent::tbx:conceptEntry or parent::tbx:termSec)">
                crossReference must be declared at concept or term levels.
            </report>
			<!-- this error message is displayed when ref is moved to language level. But corresponding message is not displayed when POS is moved to wrong level.
			Is that because in TBX-core ref is allowed at language level? -->
        </rule>
    </pattern>
    
    <pattern id="termNoteTypeAttr">
        <rule context="tbx:termNote">
            <assert test="@type='grammaticalGender' or @type='geographicalUsage' or @type='termLocation' or @type='termType' or @type='usageStatus' or @type='administrativeStatus' or @type='partOfSpeech'">
                termNote @type must take one of the following values: 'grammaticalGender', 'geographicalUsage', 'termLocation', 'termType', 'usageStatus' (formerly: 'administrativeStatus'), 'partOfSpeech'
            </assert>
            <!-- removed "epicene" -->
            <report test="@type='grammaticalGender' and (text()!='feminine' and text()!='masculine' and text()!='neuter' and text()!='other')">
                grammaticalGender must take one of the following values: feminine, masculine, or other 
            </report>
            <!-- removed all parts here and elsewhere about termNoteGrp - this element not allowed in TBX-Basic-->
            <report test="(@type='grammaticalGender') and not(parent::tbx:termSec)">
                grammaticalGender must be declared at term level.
            </report>
            
            <report test="(@type='geographicalUsage') and not(parent::tbx:termSec)">
                geographicalUsage must be declared at term level.
            </report>
            
            <report test="(@type='termLocation') and not(parent::tbx:termSec)">
                termLocation must be declared at term level.
            </report>
            
            <report test="@type='termType' and (text()!='fullForm' and text()!='acronym' and 
                text()!='abbreviation' and text()!='shortForm' and text()!='variant' and text()!='phrase')">
                termType must take one of the following values: fullForm, acronym, abbreviation, shortForm, variant, phrase.
            </report>
            <report test="(@type='termType') and not(parent::tbx:termSec)">
                termType must be declared at term level.
            </report>

            <report test="@type='administrativeStatus'" role="info">
                'usageStatus' is preferred over 'administrativeStatus'
            </report>
            <report test="@type='usageStatus' and (text()!='preferred' and text()!='admitted' and text()!='deprecated')">
                usageStatus must take one of the following values: preferred, admitted (=correct), deprecated (=avoid). 
            </report>
            <report test="(@type='usageStatus' or @type='administrativeStatus') and not(parent::tbx:termSec)">
                usageStatus (formerly: administrativeStatus) must be declared at term level.
            </report>
            
            <report test="@type='partOfSpeech' and (text()!='noun' and text()!='verb' and text()!='adjective' and text()!='adverb' and text()!='properNoun' and text()!='other')">
                partOfSpeech must take one of the following values: noun, verb, adjective, adverb, properNoun or other.
            </report>
            <report test="(@type='partofSpeech') and not(parent::tbx:termSec)">
                partOfSpeech must be declared at term level.
            </report>
			<!-- an error is reported when moved to other levels, but not with this message. A generic error is displayed. I believe it is because the (some?) levels are checked by the core schema. But not all levels declarations here are redundant, see comment at ref-->
        </rule>
    </pattern>
    
    <pattern id="transacNoteTypeAttr">
        <rule context="tbx:transacNote">
            <assert test="@type='responsibility'">
                transacNote @type must take the value: 'responsibility'
            </assert>
            <report test="(@type='responsibility') and not(parent::tbx:transacGrp[parent::tbx:conceptEntry or parent::tbx:langSec or parent::tbx:termSec])">
                transacNote type='responsibility' must be nested inside of transacGrp.
            </report>
        </rule>
    </pattern>
    
    <pattern id="transacTypeAttr">
        <rule context="tbx:transac">
            <assert test="@type='transactionType'">
                transac @type must take the value: 'transactionType'
            </assert>
            <report test="@type='transactionType' and (text()!='creation' and text()!='modification')">
                transactionType must take one of the following values: creation, modification
            </report>
            <report test="(@type='transactionType') and not(parent::tbx:transacGrp[parent::tbx:conceptEntry or parent::tbx:langSec or parent::tbx:termSec])">
                transactionType must be nested inside of transacGrp.
            </report>
        </rule>
    </pattern>
    
    <pattern id="xrefTypeAttr">
	<!-- what about the target attribute?-->
        <rule context="tbx:xref">
            <assert test="@type='xGraphic' or @type='externalCrossReference'">
                xref @type must take one of the following values: 'xGraphic', 'externalCrossReference'
            </assert>
            <report test="(@type='xGraphic') and not(parent::tbx:conceptEntry)">
                xGraphic must be declared at concept level.
            </report>
            <report test="(@type='externalCrossReference') and not(parent::tbx:conceptEntry or parent::tbx:termSec)">
                externalCrossReference must be declared at concept or term levels.
            </report>
        </rule>
    </pattern>
    
    
</schema>