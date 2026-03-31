import streamlit as st

def main():
    st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap');

        /* Apply font to app text */
        .stApp, h1, h2, h3, h4, h5, h6, p, span, label, div ,li,ul{
            font-family: 'JetBrains Mono', monospace;
        }
        </style>
    """,unsafe_allow_html=True)

    st.set_page_config(page_title="Explanation", layout="wide")

    st.title("Explanation")
    st.markdown("---")

    # ---------------- INTRO ---------------- #
    st.header("Overview")

    st.write("""
    This project implements a **_simple RISC assembler_** in Python.
             
    The purpose of this assembler is to convert assembly language instructions into 
    their corresponding **_32-bit binary machine code_**.

    The assembler has **_two-steps_** for the execution of the program:
    - First Step: Identify labels and store their addresses
    - Second Step: Convert instructions into machine code using those labels
    """)

    # ----------EXAMPLE TITLE ---------- #
    st.title("Example: Assembly to Machine Code Conversion")
    st.markdown("---")

    # ---------- INPUT CODE ----------
    st.header("Example")

    st.code("""
    START:  MOV R1, 5
            MOV R2, 0

    LOOP:   ADD R2, R2, R1
            SUB R1, R1, 1

            CMP R1, 0
            BGT LOOP

    END:    HLT
    """, language="assembly")

    st.markdown("""
    This example demonstrates how a simple assembly program is converted into 
    *32-bit machine code* using the assembler.
    """)

    # ---------- FIRST STEP ----------
    st.header("2. First Step: Label Detection")
    # ---------- INITIAL STATE ----------
    st.subheader("Initial State")

    st.code("""
    instruction_address = 0
    labels = {}
    """, language="text")


    # ---------- LINE 1 ----------
    st.subheader("Line 1: START: MOV R1, 5")

    st.markdown("""
    *Label detected:* `START`  
    Stored as:
    """)
    st.code("START → 0", language="text")

    st.markdown("Instruction exists → increment address")
    st.code("instruction_address = 1", language="text")


    # ---------- LINE 2 ----------
    st.subheader("Line 2: MOV R2, 0")

    st.markdown("""
    No label detected.  
    Instruction exists → increment address
    """)

    st.code("instruction_address = 2", language="text")


    # ---------- LINE 3 ----------
    st.subheader("Line 3: LOOP: ADD R2, R2, R1")

    st.markdown("""
    *Label detected:* `LOOP`  
    Stored as:
    """)

    st.code("LOOP → 2", language="text")

    st.markdown("Instruction exists → increment address")

    st.code("instruction_address = 3", language="text")


    # ---------- LINE 4 ----------
    st.subheader("Line 4: SUB R1, R1, 1")

    st.markdown("""
    No label detected.  
    Instruction exists → increment address
    """)

    st.code("instruction_address = 4", language="text")


    # ---------- LINE 5 ----------
    st.subheader("Line 5: CMP R1, 0")

    st.markdown("""
    No label detected.  
    Instruction exists → increment address
    """)

    st.code("instruction_address = 5", language="text")


    # ---------- LINE 6 ----------
    st.subheader("Line 6: BGT LOOP")

    st.markdown("""
    No new label detected.  
    Instruction exists → increment address
    """)

    st.code("instruction_address = 6", language="text")


    # ---------- LINE 7 ----------
    st.subheader("Line 7: END: HLT")

    st.markdown("""
    *Label detected:* `END`  
    Stored as:
    """)

    st.code("END → 6", language="text")

    st.markdown("Instruction exists → increment address")

    st.code("instruction_address = 7", language="text")


    # ---------- FINAL LABEL TABLE ----------
    st.subheader("Final Label Table")

    st.table({
        "Label": ["START", "LOOP", "END"],
        "Address": [0, 2, 6]
    })

    # ---------- SECOND STEP ----------
    st.header("3. Second Step: Instruction Encoding")

    st.markdown("""
    During the *second step*, each instruction is converted into its corresponding 
    32-bit machine code.

    The assembler:
    - Identifies the instruction type  
    - Selects the appropriate encoding function  
    - Converts registers and immediate values into binary  
    - Resolves labels using the label table from the first pass  
    """)

    st.subheader("Function Selection Logic")

    st.code("""
    if inst in ["CALL", "B", "BEQ", "BGT"]:
        → one_address_instruction()

    elif inst in ["ADD", "SUB", ...]:
        → three_address_instruction()

    elif inst in ["CMP", "NOT", "MOV"]:
        → two_address_instruction()

    elif inst in ["LD", "ST"]:
        → load_store_instruction()

    elif inst in ["NOP", "RET", "HLT"]:
        → zero_address_instruction()
    """, language="python")

    st.subheader("Step-by-Step Instruction Encoding")
    st.markdown("### Instruction 1: MOV R1, 5")

    st.markdown("""
    *Instruction Type:* Two-address  
    *Function Used:* `two_address_instruction()`  
    """)

    st.markdown("""
    - Opcode → `01001`  
    - RI_Type → `1` *(immediate)*  
    - R1 → `0001`  
    - Immediate 5 → `0000000000000101`  
    """)

    st.code("01001100010000000000000000000101", language="text")

    st.markdown("### Instruction 2: MOV R2, 0")

    st.markdown("""
    *Instruction Type:* Two-address  
    *Function Used:* `two_address_instruction()`  
    """)

    st.markdown("""
    - Opcode → `01001`  
    - RI_Type → `1`  
    - R2 → `0010`  
    - Immediate 0 → `0000000000000000`  
    """)

    st.code("01001100100000000000000000000000", language="text")

    st.markdown("### Instruction 3: ADD R2, R2, R1")

    st.markdown("""
    *Instruction Type:* Three-address  
    *Function Used:* `three_address_instruction()`  
    """)

    st.markdown("""
    - Opcode → `00000`  
    - RI_Type → `0` *(register)*  
    - R2 → `0010`  
    - R2 → `0010`  
    - R1 → `0001`  
    """)

    st.code("00000000100010000100000000000000", language="text")

    st.markdown("### Instruction 4: SUB R1, R1, 1")

    st.markdown("""
    *Instruction Type:* Three-address  
    *Function Used:* `three_address_instruction()`  
    """)

    st.markdown("""
    - Opcode → `00001`  
    - RI_Type → `1` *(immediate)*  
    - R1 → `0001`  
    - R1 → `0001`  
    - Immediate 1 → `0000000000000001`  
    """)

    st.code("00001100010001000000000000000001", language="text")

    st.markdown("### Instruction 5: CMP R1, 0")

    st.markdown("""
    *Instruction Type:* Two-address  
    *Function Used:* `two_address_instruction()`  
    """)

    st.markdown("""
    - Opcode → `00101`  
    - RI_Type → `1`  
    - R1 → `0001`  
    - Immediate 0 → `0000000000000000`  
    """)

    st.code("00101100010000000000000000000000", language="text")

    st.header("Relative Addressing (Branch Instruction)")

    st.markdown("""
    Branch instructions such as `BGT` use *relative addressing*.

    Instead of storing the absolute address, the assembler stores the 
    *offset* between the target label and the current instruction.
    """)

    st.markdown("### Instruction 6: BGT LOOP")

    st.markdown("""
    *Instruction Type:* One-address  
    *Function Used:* `one_address_instruction()`  
    """)

    st.markdown("""
    The offset is calculated as:

    *offset = target_address − current_PC*
    """)

    st.markdown("""
    From the label table:

    - LOOP address = `2`  
    - Current PC (BGT instruction) = `6`  

    So,
    """)
    st.code("offset = 2 - 6 = -4", language="text")

    st.markdown("""
    Since the offset is negative, it is converted into *two’s complement form*.
    """)

    st.code("""
    -4 in binary (27-bit) → 111111111111111111111111100
    """, language="text")

    st.markdown("""
    - Opcode (BGT) → `10001`  
    - Offset → 27-bit binary  
    """)

    st.code("100011111111111111111111110011100", language="text")

    st.markdown("### Instruction 7: HLT")

    st.markdown("""
    *Instruction Type:* Zero-address  
    *Function Used:* `zero_address_instruction()`  
    """)

    st.code("11111000000000000000000000000000", language="text")
    # ---------- FINAL OUTPUT ----------#
    st.header("4. Final Machine Code Output")

    st.code("""
    01001100010000000000000000000101
    01001100100000000000000000000000
    00000000100010000100000000000000
    00001100010001000000000000000001
    00101100000001000000000000000000
    10001111111111111111111110011100
    11111000000000000000000000000000
    """, language="text")

    # ---------- CONCLUSION ----------
    st.header("Key Takeaways")

    st.markdown("""

    - Labels are resolved before encoding instructions  
    - Each instruction is converted into a fixed *32-bit format*  
    - Different instruction types use different encoding strategies  
    """)
    st.success("End of Explanation")
if __name__ == "__main__":
     main()