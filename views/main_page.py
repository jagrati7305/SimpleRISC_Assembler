import streamlit as st
from assembler import init, collect_labels_and_loops, assemble_line, remove_comments


def assemble_code(lines):
    init()
    collect_labels_and_loops(lines)

    machine_code = []
    errors = []

    for line in lines:
        clean_line = remove_comments(line)
        if clean_line.strip() == "":
            continue
        machine_code_line = assemble_line(line)
        if machine_code_line and not machine_code_line.startswith("ERROR"):
            machine_code.append(machine_code_line)
        elif machine_code_line and machine_code_line.startswith("ERROR"):
            errors.append(f"{line.strip()}  --> {machine_code_line}")

    return machine_code, errors


def to_hex_output(machine_code):
    hex_lines = []
    for code_line in machine_code:
        if "-->" in code_line:
            continue
        try:
            hex_val = hex(int(code_line, 2))[2:].upper().zfill(8)
            hex_lines.append(f"0x{hex_val}")
        except ValueError:
            continue
    return hex_lines


def main():
    st.set_page_config(page_title="TinyRISC Assembler", layout="wide")

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap');

    .stApp, h1, h2, h3, h4, h5, h6, p, span, label, div {
        font-family: 'JetBrains Mono', monospace;
    }

    .material-icons {
        font-family: 'Material Icons' !important;
    }

    div.stButton > button:first-child {
        background-color: #ffffff;
        color: #181818;
        border-radius: 8px;
        width: 100%;
        height: 3em;
        font-size: 16px;
    }

    div.stButton > button:hover {
        background-color: #0D0D0D;
        color: #ffffff;
        border: 2px solid white;
    }

    [data-testid="stFileUploader"] button {
        background-color: #ffffff;
        color: #181818;
    }

    [data-testid="stFileUploader"] button:hover {
        background-color: #0D0D0D;
        color: #ffffff;
        border: 2px solid white;
    }

    [data-testid="stFileUploader"] {
        background-color: #646464;
        padding: 2px;
        border-radius: 8px;
    }

    textarea {
        border: 2px solid #646464 !important;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Editor")

    with st.container(border=True):
        st.write("Upload your `.asm` file or write code manually.")
        st.write("You can also edit uploaded code before assembling.")

        uploaded_code = ""
        uploaded_file = st.file_uploader("Upload File", label_visibility="collapsed", type=["asm"])

        if uploaded_file is not None:
            uploaded_code = uploaded_file.read().decode("utf-8")

        st.write("Edit or Write your Assembly Code")
        code_area = st.text_area(
            "Assembly Code",
            label_visibility="collapsed",
            height=300,
            placeholder="~/ Prakritti >",
            value=uploaded_code,
        )

    assemble_code_btn = st.button("Assemble Code")

    if assemble_code_btn:
        if not code_area.strip():
            st.warning("Please upload or write some Assembly code first.")
            return

        lines = code_area.splitlines()

        try:
            machine_code, errors = assemble_code(lines)

            if errors:
                st.error("❌ Assembly failed with errors:")
                for err in errors:
                    st.code(err)
                return

            # Build binary data for download
            binary_data = bytearray()
            for code_line in machine_code:
                try:
                    byte_value = int(code_line, 2)
                    binary_data += byte_value.to_bytes(4, byteorder="big")
                except ValueError:
                    continue

            # Build hex output
            hex_output = to_hex_output(machine_code)

            st.session_state["machine_code"] = machine_code
            st.session_state["binary_data"] = binary_data
            st.session_state["hex_output"] = hex_output

            st.success("✅ Assembly successful!")

        except Exception as e:
            st.error(f"❌ Error during assembly: {e}")

    # ── Output section ────────────────────────────────────────────────────────
    if "machine_code" in st.session_state:
        machine_code = st.session_state["machine_code"]
        binary_data  = st.session_state["binary_data"]
        hex_output   = st.session_state["hex_output"]

        binary_text = "\n".join(machine_code)
        hex_text    = "\n".join(hex_output)

        st.header("Output")

        # Side-by-side text areas
        col_bin, col_hex = st.columns(2)

        with col_bin:
            st.subheader("Binary")
            st.text_area(
                "Binary Output",
                label_visibility="collapsed",
                height=300,
                value=binary_text,
            )

        with col_hex:
            st.subheader("Hexadecimal")
            st.text_area(
                "Hex Output",
                label_visibility="collapsed",
                height=300,
                value=hex_text,
            )

        # Download buttons
        dl_bin, dl_hex = st.columns(2)

        with dl_bin:
            st.download_button(
                label="Download Binary (.bin)",
                data=binary_text.encode("utf-8"), 
                file_name="output.bin",
                mime="text/plain",
                use_container_width=True,
            )
        with dl_hex:
            st.download_button(
                label="Download Hex (.hex)",
                data=hex_text.encode("utf-8"),
                file_name="output.hex",
                mime="text/plain",
                use_container_width=True,
            )


if __name__ == "__main__":
    main()