# Copyright 2023 AUC Open Source Hardware Lab
#
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at:
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import os
from pyeda.inter import *
import copy
from sympy.logic import simplify_logic as simplifyLogic
from sympy import parse_expr
from sympy import SOPform, bool_map
from liberty.parser import parse_liberty as parseLiberty

##########################################################################################


class CellRepresentation:
    def __init__(self, name, function, svgFile):
        self.name = name
        self.function = function
        self.svgFile = svgFile


##########################################################################################


def reformatBooleanExpression(expression):
    for char in expression:
        if char == '"':
            expression = expression.replace('"', "")
        elif char == "!":
            expression = expression.replace("!", "~")
        elif char == "*":
            expression = expression.replace("*", "&")
        # todo check the right way of replacing the space operator
        # elif char == ' ':
        #    expression = expression.replace(' ', '&')
        elif char == "+":
            expression = expression.replace("+", "|")
        elif char == "^":
            expression = expression.replace("^", "^")
        elif char == "(":
            expression = expression.replace("(", "(")
        elif char == ")":
            expression = expression.replace(")", ")")
        elif char == "S":
            expression = expression.replace("S", "replaced")
        elif char == "s":
            expression = expression.replace("s", "replaced")
    return expression


##########################################################################################
def writeCellSVG(dirPath, cell_group, cellRepRef):

    f = open("./representations/" + cellRepRef.svgFile, "r")
    svgRep = f.read()
    cellName = str(cell_group.args[0])
    cleanedCellName = str(cellName).replace('"', "")
    print("writing " + cleanedCellName)
    svgRep = svgRep.replace("name", cleanedCellName)
    
    alias = '''<s:alias val="''' + cleanedCellName + '''"/>'''
    svgRep = svgRep.replace("alias", alias)
    
    inputPinCount = 0
    outputPinCount = 0
    for pinGroup in cell_group.get_groups("pin"):
        pinName = pinGroup.args[0]
        if pinGroup["direction"] == "input":
            inputPinCount = inputPinCount + 1
            pinReplacer = "input" + str(inputPinCount)
            cleanedPinName = str(pinName).replace('"', "")
            svgRep = svgRep.replace(pinReplacer, cleanedPinName)
            # print("replacing "+ str(pinName))
        if pinGroup["direction"] == "output":
            outputPinCount = outputPinCount + 1
            pinReplacer = "output" + str(outputPinCount)
            cleanedPinName = str(pinName).replace('"', "")
            svgRep = svgRep.replace(pinReplacer, cleanedPinName)
            # print("replacing "+ str(pinName))

    with open(dirPath + "/default.svg", "a") as f:
        f.write(svgRep + "\n\n")


##########################################################################################


def writeLibraryDefaultSVG(tobeWritten, libraryName):
    dirpath = "./" + libraryName + "_representations"
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    with open(dirpath + "/default.svg", "w") as f:
        f.write(
            """
 <svg  xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:s="https://github.com/nturley/netlistsvg"
  width="800" height="300">
  <s:properties>
    <s:layoutEngine
      org.eclipse.elk.layered.spacing.nodeNodeBetweenLayers="35"
      org.eclipse.elk.spacing.nodeNode= "35"
      org.eclipse.elk.layered.layering.strategy= "LONGEST_PATH"
    />
    <s:low_priority_alias val="$dff" />
  </s:properties>
<style>
svg {
  stroke:#000;
  fill:none;
}
text {
  fill:#000;
  stroke:none;
  font-size:10px;
  font-weight: bold;
  font-family: "Courier New", monospace;
}
.nodelabel {
  text-anchor: middle;
}
.inputPortLabel {
  text-anchor: end;
}
.splitjoinBody {
  fill:#000;
}
</style>
                """
        )

    for cell in tobeWritten:
        writeCellSVG(dirpath, cell[0], cell[1])

    with open(dirpath + "/default.svg", "a") as f:
        f.write(
            """

  <g s:type="lt" transform="translate(50,200)" s:width="25" s:height="25">
    <s:alias val="$lt"/>

    <circle r="12.5" cx="12.5" cy="12.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="12.5" y2="7.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="12.5" y2="17.5" class="$cell_id"/>

    <g s:x="3" s:y="5" s:pid="A"/>
    <g s:x="3" s:y="20" s:pid="B"/>
    <g s:x="25" s:y="12.5" s:pid="Y"/>
  </g>

  <g s:type="le" transform="translate(150,200)" s:width="25" s:height="25">
    <s:alias val="$le"/>

    <circle r="12.5" cx="12.5" cy="12.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="12.5" y2="7.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="12.5" y2="17.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="15" y2="20" class="$cell_id"/>

    <g s:x="3" s:y="5" s:pid="A"/>
    <g s:x="3" s:y="20" s:pid="B"/>
    <g s:x="25" s:y="12.5" s:pid="Y"/>
  </g>

  <g s:type="ge" transform="translate(250,200)" s:width="25" s:height="25">
    <s:alias val="$ge"/>

    <circle r="12.5" cx="12.5" cy="12.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="7.5" y2="12.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="17.5" y2="12.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="20" y2="15" class="$cell_id"/>

    <g s:x="3" s:y="5" s:pid="A"/>
    <g s:x="3" s:y="20" s:pid="B"/>
    <g s:x="25" s:y="12.5" s:pid="Y"/>
  </g>

  <g s:type="gt" transform="translate(350,200)" s:width="25" s:height="25">
    <s:alias val="$gt"/>

    <circle r="12.5" cx="12.5" cy="12.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="7.5" y2="12.5" class="$cell_id"/>
    <line x1="7.5" x2="17.5" y1="17.5" y2="12.5" class="$cell_id"/>

    <g s:x="3" s:y="5" s:pid="A"/>
    <g s:x="3" s:y="20" s:pid="B"/>
    <g s:x="25" s:y="12.5" s:pid="Y"/>
  </g>

  <g s:type="inputExt" transform="translate(50,250)" s:width="30" s:height="20">
    <text x="15" y="-4" class="nodelabel $cell_id" s:attribute="ref">input</text>
    <s:alias val="$_inputExt_"/>
    <path d="M0,0 L0,20 L15,20 L30,10 L15,0 Z" class="$cell_id"/>
    <g s:x="28" s:y="10" s:pid="Y"/>
  </g>

  <g s:type="constant" transform="translate(150,250)" s:width="30" s:height="20">
    <text x="15" y="-4" class="nodelabel $cell_id" s:attribute="ref">constant</text>

    <s:alias val="$_constant_"/>
    <rect width="30" height="20" class="$cell_id"/>

    <g s:x="30" s:y="10" s:pid="Y"/>
  </g>

  <g s:type="outputExt" transform="translate(250,250)" s:width="30" s:height="20">
    <text x="15" y="-4" class="nodelabel $cell_id" s:attribute="ref">output</text>
    <s:alias val="$_outputExt_"/>
    <path d="M30,0 L30,20 L15,20 L0,10 L15,0 Z" class="$cell_id"/>

    <g s:x="0" s:y="10" s:pid="A"/>
  </g>

  <g s:type="split" transform="translate(350,250)" s:width="5" s:height="40">
    <rect width="5" height="40" class="splitjoinBody" s:generic="body"/>
    <s:alias val="$_split_"/>

    <g s:x="0" s:y="20" s:pid="in"/>
    <g transform="translate(5, 10)" s:x="4" s:y="10" s:pid="out0">
      <text x="5" y="-4">hi:lo</text>
    </g>
    <g transform="translate(5, 30)" s:x="4" s:y="30" s:pid="out1">
      <text x="5" y="-4">hi:lo</text>
    </g>
  </g>

  <g s:type="join" transform="translate(450,250)" s:width="4" s:height="40">
    <rect width="5" height="40" class="splitjoinBody" s:generic="body"/>
    <s:alias val="$_join_"/>
    <g s:x="5" s:y="20"  s:pid="out"/>
    <g transform="translate(0, 10)" s:x="0" s:y="10" s:pid="in0">
      <text x="-3" y="-4" class="inputPortLabel">hi:lo</text>
    </g>
    <g transform="translate(0, 30)" s:x="0" s:y="30" s:pid="in1">
      <text x="-3" y="-4" class="inputPortLabel">hi:lo</text>
    </g>
  </g>

  <g s:type="generic" onClick="reply_click(this.id)" transform="translate(550,250)" s:width="30" s:height="40">
    <text x="15" y="-4" class="nodelabel $cell_id" s:attribute="ref">generic</text>
    <rect width="30" height="40" s:generic="body" class="$cell_id"/>

    <g transform="translate(30, 10)" s:x="30" s:y="10" s:pid="out0">
      <text x="5" y="-4" style="fill:#000; stroke:none" class="$cell_id">out0</text>
    </g>
    <g transform="translate(30, 30)" s:x="30" s:y="30" s:pid="out1">
      <text x="5" y="-4" style="fill:#000;stroke:none" class="$cell_id">out1</text>
    </g>
    <g transform="translate(0, 10)" s:x="0" s:y="10" s:pid="in0">
      <text x="-3" y="-4" class="inputPortLabel $cell_id">in0</text>
    </g>
    <g transform="translate(0, 30)" s:x="0" s:y="30" s:pid="in1">
      <text x="-3" y="-4" class="inputPortLabel $cell_id">in1</text>
    </g>
  </g>

</svg>
                """
        )

        pass


##########################################################################################
# Main Class
def main():
    cellRepresentations = [
        CellRepresentation("AND2", "A&B", "AND2.svg"),
        CellRepresentation("AND2b", "(~A_N&B)", "AND2b.svg"),
        CellRepresentation("AND3", "A&B&C", "AND3.svg"),
        CellRepresentation("AND3b", "(~A_N&B&C)", "AND3b.svg"),
        CellRepresentation("AND4", "A&B&C&D", "AND4.svg"),
        CellRepresentation("AND4b", "(~A_N&B&C&D)", "AND4b.svg"),
        CellRepresentation("AND4bb", "(~A_N&~B_N&C&D)", "AND4bb.svg"),
        CellRepresentation("OR2", "A|B", "OR2.svg"),
        CellRepresentation("OR2b", "(A)|(~B_N)", "OR2b.svg"),
        CellRepresentation("OR3", "A|B|C", "OR3.svg"),
        CellRepresentation("OR3b", "(A)|(B)|(~C_N)", "OR3b.svg"),
        CellRepresentation("OR4", "A|B|C|D", "OR4.svg"),
        CellRepresentation("OR4b", "(A)|(B)|(C)|(~D_N)", "OR4b.svg"),
        CellRepresentation("OR4bb", "(A)|(B)|(~C_N)|(~D_N)", "OR4bb.svg"),
        CellRepresentation("NAND2", "~(A&B)", "NAND2.svg"),
        CellRepresentation("NAND2b", "(A_N)|(~B)", "NAND2b.svg"),
        CellRepresentation("NAND3", "~(A&B&C)", "NAND3.svg"),
        CellRepresentation("NAND3b", "(A_N)|(~B)|(~C)", "NAND3b.svg"),
        CellRepresentation("NAND4", "~(A&B&C&D)", "NAND4.svg"),
        CellRepresentation("NAND4b", "(A_N)|(~B)|(~C)|(~D)", "NAND4b.svg"),
        CellRepresentation("NAND4bb", "(A_N)|(B_N)|(~C)|(~D)", "NAND4bb.svg"),
        CellRepresentation("NOR2", "~(A|B)", "NOR2.svg"),
        CellRepresentation("NOR2b", "(~A&B_N)", "NOR2b.svg"),
        CellRepresentation("NOR3", "~(A|B|C)", "NOR3.svg"),
        CellRepresentation("NOR3b", "(~A&~B&C_N)", "NOR3b.svg"),
        CellRepresentation("NOR4", "~(A|B|C|D)", "NOR4.svg"),
        CellRepresentation("NOR4b", "(~A&~B&~C&D_N)", "NOR4b.svg"),
        CellRepresentation("NOR4bb", "(~A&~B&C_N&D_N)", "NOR4bb.svg"),
        # CellRepresentation("XOR2", "A^B", "XOR2.svg"),
        # CellRepresentation("XOR3", "A^B^C", "XOR3.svg"),
        # CellRepresentation("XOR4", "A^B^C^D", "XOR4.svg"),
        # CellRepresentation("XNOR2", "~(A^B)", "XNOR2.svg"),
        # CellRepresentation("XNOR3", "~(A^B^C)", "XNOR3.svg"),
        # CellRepresentation("XNOR4", "~(A^B^C^D)", "XNOR4.svg"),
        CellRepresentation("INV", "~A", "INV.svg"),
        CellRepresentation("BUF", "A", "BUF.svg"),
        CellRepresentation("MUX2", "(A0&~sel)|(A1&sel)", "MUX2.svg"),
        CellRepresentation(
            "MUX4",
            "(A0&~sel0&~sel1)|(A1&sel0&~sel1)|(A2&~sel0&sel1)|(A3&sel0&sel1)",
            "MUX4.svg",
        ),
        CellRepresentation(
            "MUX8",
            "(A0&~sel0&~sel1&~sel2)|(A1&sel0&~sel1&~sel2)|(A2&~sel0&sel1&~sel2)|(A3&sel0&sel1&~sel2)|(A4&~sel0&~sel1&sel2)|(A5&sel0&~sel1&sel2)|(A6&~sel0&sel1&sel2)|(A7&sel0&sel1&sel2)",
            "MUX8.svg",
        ),
        CellRepresentation("MUX2i", "(~A0&~sel) | (~A1&sel)", "MUX2i.svg"),
    ]
    #####################################

    libertyFile = "/Users/youssef/Documents/Work/AUC_Open_Hardware_Lab/interactive_sVG_schematics/liberty/sky130_fd_sc_hd.lib"
    # Read and parse a library.
    library = parseLiberty(open(libertyFile).read())

    tobeWritten = []

    for cell_group in library.get_groups("cell"):
        is_flipflop = (len(cell_group.get_groups("ff"))) != 0
        is_latch = (len(cell_group.get_groups("latch"))) != 0
        is_isolation_cell = cell_group["is_isolation_cell"] != None
        is_level_shifter = cell_group["is_level_shifter"] != None

        # print(is_isolation_cell,cell_group["is_isolation_cell"] )
        if is_flipflop:
            pass
        elif is_latch:
            pass
        elif is_level_shifter:
            pass
        elif is_isolation_cell:
            pass
        else:
            # print(cell_group.get_groups("ff"))
            outputPinCounter = 0
            cellRepRef = None
            flag = False
            pinRef = None
            translationRef = None
            for pinGroup in cell_group.get_groups("pin"):
                if pinGroup["direction"] == "output":
                    outputPinCounter += 1
                    if pinGroup["function"] is not None:
                        iterationLibraryCellFunction = reformatBooleanExpression(
                            copy.copy(str(pinGroup["function"]))
                        )
                        # print(iterationLibraryCellFunction)

                        for cell in cellRepresentations:
                            new_library_cell_function = reformatBooleanExpression(
                                copy.copy(cell.function)
                            )
                            function1 = parse_expr(iterationLibraryCellFunction)
                            function2 = parse_expr(new_library_cell_function)
                            simplifyLogic(function1)
                            simplifyLogic(function2)
                            out = bool_map(function1, function2)
                            if (out != None) and (out != False):
                                flag = True
                                cellRepRef = cell
                                pinRef = pinGroup
                                translationRef = out

            if (outputPinCounter == 1) & (flag == True):
                tobeWritten.append([copy.copy(cell_group), copy.copy(cellRepRef)])

                # print(
                #    "cell name: ",
                #    cell_group.args[0],
                #    "pin name: ",
                #    pinRef.args[0],
                #    "function: ",
                #    pinRef["function"],
                #    "new function: ",
                #    cellRepRef.function,
                #    "translation: ",
                #    translationRef,
                #    "svg: ",
                #    cellRepRef.svgFile,
                # )

    libraryName = copy.copy(libertyFile)
    libraryName = libraryName.split("/")[-1]
    libraryName = libraryName.split(".")[0]
    writeLibraryDefaultSVG(tobeWritten, libraryName)


if __name__ == "__main__":
    main()
