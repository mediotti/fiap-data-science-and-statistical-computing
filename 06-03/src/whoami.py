from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Greeting Dashboard - Gabriel Mediotti", layout="wide")
st.sidebar.markdown("Desenvolvido por Gabriel Mediotti - [Github](https://github.com/mediotti)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        # `~$ whoami`

Over the years, I've come to realize that my fascination with computing predates even my earliest lines of code, typed in Python when I was around 15 or 16. Perhaps it stemmed from my childhood curiosity about what lurked inside a video game console, or my unquenchable desire to assemble my own computers during those pre-teen years. It might even have originated from my failed attempts at salvaging hard drives or constructing gadgets that only made sense in my mind. But it was through these experiences that I discovered the power of code – the freedom to create, to shape the digital world to my will.

In the realm of bits and bytes, that's who I am. My name is Gabriel, born and raised in São Paulo. For years, I've poured my energy into crafting software that has the potential to reshape society's dynamics. In this short span, I've had the privilege to contribute to the development of cutting-edge systems in IoT, tailored for the Energy and Smart Cities sectors.

Academically, I had the opportunity to study at the Federal Technological University of Paraná, where I started to pursue a degree in Computer Engineering. During my time there, I actively engaged with the community, volunteering at hackathons and other events. However, my professional trajectory diverged from my academic path, leading me to realize that to truly advance in my career, I needed to return to São Paulo. Now, as I write this, I am a student of Software Engineering at FIAP, proudly supported by a PROUNI scholarship.

My recent focus has led me to dive into fascinating topics such as Distributed Systems, Computer Networks, and Data Compression. In my spare time, I'm dedicated to developing solutions that encompass these areas of interest.

I hope that my journey serves as an inspiration, and that the knowledge I've gained along the way can be harnessed for positive change in the world.
        """
    )

with col2:
    st.image("../assets/me.png")