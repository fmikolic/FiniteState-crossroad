#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import random
import time
from random import randint
from termcolor import colored
from asyncio import sleep

import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State


class PonasanjeKA(FSMBehaviour):
    async def on_start(self):
        print("Zapocinjem ponasanje PRVOG konacnog automata.")

    async def on_end(self):
        print("Zavrsavam ponasanje PRVOG konacnog automata.")
        await self.agent.stop()

class CrvenoStanje(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg.body=="Priprema":
            print(colored(self.oznaka, 'red'))
        else:
            print(f"{self.oznaka} : {msg.body}")
        
        self.set_next_state("ZutoStanje")

class ZutoStanje(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg.body=="Kreni":
            print(colored(self.oznaka, 'yellow'))
        else:
            print(f"{self.oznaka} : {msg.body}")
        
        self.set_next_state("ZelenoStanje")

class ZutoStanje2(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg.body=="Stop":
            print(colored(self.oznaka, 'yellow'))
        else:
            print(f"{self.oznaka} : {msg.body}")
        
        self.set_next_state("CrvenoStanje")

class ZelenoStanje(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg.body=="Priprema2":
            print(colored(self.oznaka, 'green'))
        else:
            print(f"{self.oznaka} : {msg.body}")
        
        self.set_next_state("ZutoStanje2")



class PCrvenoStanje(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg.body=="Kreni":
            print(colored(self.oznaka, 'red'))
        else:
            print(f"{self.oznaka} : {msg.body}")
        
        
        self.set_next_state("PZelenoStanje")


class PZelenoStanje(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg.body=="Stop":
            print(colored(self.oznaka, 'green'))
        else:
            print(f"{self.oznaka} : {msg.body}")
        
        
        self.set_next_state("PCrvenoStanje")

class AgentAutomat1(Agent):
    async def setup(self):
        print("Prvi prometni semafor (SMJER 1) krece u akciju!")
        #oznakaSemafora="Prometni semafor 1"
        oznakaSemafora="1. 🚗"
        fsm = PonasanjeKA()
        cstanje=CrvenoStanje()
        cstanje.oznaka=oznakaSemafora
        fsm.add_state(name="CrvenoStanje", state=cstanje, initial=True)

        zustanje=ZutoStanje()
        zustanje.oznaka=oznakaSemafora
        fsm.add_state(name="ZutoStanje", state=zustanje)

        zestanje=ZelenoStanje()
        zestanje.oznaka=oznakaSemafora
        fsm.add_state(name="ZelenoStanje", state=zestanje)

        zu2stanje=ZutoStanje2()
        zu2stanje.oznaka=oznakaSemafora
        fsm.add_state(name="ZutoStanje2", state=zu2stanje)

        fsm.add_transition(source="CrvenoStanje", dest="ZutoStanje")
        fsm.add_transition(source="ZutoStanje", dest="ZelenoStanje")
        fsm.add_transition(source="ZelenoStanje", dest="ZutoStanje2")
        fsm.add_transition(source="ZutoStanje2", dest="CrvenoStanje")

        self.add_behaviour(fsm)

class AgentAutomat2(Agent):
    async def setup(self):
        print("Drugi prometni semafor (SMJER 2) krece u akciju!")
        #oznakaSemafora="      Prometni semafor 2"
        oznakaSemafora="       2. 🚗"
        fsm = PonasanjeKA()
        cstanje=CrvenoStanje()
        cstanje.oznaka=oznakaSemafora
        fsm.add_state(name="CrvenoStanje", state=cstanje)

        zustanje=ZutoStanje()
        zustanje.oznaka=oznakaSemafora
        fsm.add_state(name="ZutoStanje", state=zustanje)

        zestanje=ZelenoStanje()
        zestanje.oznaka=oznakaSemafora
        fsm.add_state(name="ZelenoStanje", state=zestanje, initial=True)

        zu2stanje=ZutoStanje2()
        zu2stanje.oznaka=oznakaSemafora
        fsm.add_state(name="ZutoStanje2", state=zu2stanje)

        fsm.add_transition(source="CrvenoStanje", dest="ZutoStanje")
        fsm.add_transition(source="ZutoStanje", dest="ZelenoStanje")
        fsm.add_transition(source="ZelenoStanje", dest="ZutoStanje2")
        fsm.add_transition(source="ZutoStanje2", dest="CrvenoStanje")

        self.add_behaviour(fsm)



class AgentAutomat3(Agent):
    async def setup(self):
        print("Prvi pjesacki semafor (SMJER 1) krece u akciju!")
        #oznakaSemafora="Pjesacki semafor 1"
        oznakaSemafora="1. 🙎"
        fsm = PonasanjeKA()
        cstanje=PCrvenoStanje()
        cstanje.oznaka=oznakaSemafora
        fsm.add_state(name="PCrvenoStanje", state=cstanje, initial=True)

        zestanje=PZelenoStanje()
        zestanje.oznaka=oznakaSemafora
        fsm.add_state(name="PZelenoStanje", state=zestanje)

        fsm.add_transition(source="PCrvenoStanje", dest="PZelenoStanje")
        fsm.add_transition(source="PZelenoStanje", dest="PCrvenoStanje")

        self.add_behaviour(fsm)

class AgentAutomat4(Agent):
    async def setup(self):
        print("Drugi pjesacki semafor (SMJER 2) krece u akciju!")
        #oznakaSemafora="      Pjesacki semafor 2"
        oznakaSemafora="       2. 🙎"
        fsm = PonasanjeKA()
        cstanje=PCrvenoStanje()
        cstanje.oznaka=oznakaSemafora
        fsm.add_state(name="PCrvenoStanje", state=cstanje)

        zestanje=PZelenoStanje()
        zestanje.oznaka=oznakaSemafora
        fsm.add_state(name="PZelenoStanje", state=zestanje, initial=True)

        fsm.add_transition(source="PCrvenoStanje", dest="PZelenoStanje")
        fsm.add_transition(source="PZelenoStanje", dest="PCrvenoStanje")

        self.add_behaviour(fsm)



#upravljac

class PonasanjeKA1(FSMBehaviour):
    async def on_start(self):
        print("Zapocinjem ponasanje UPRAVLJACA.")

    async def on_end(self):
        print("Zavrsavam ponasanje UPRAVLJACA.")
        await self.agent.stop()


class PokreniRaskrizje(State):
    async def run(self):
        msg = spade.message.Message(to="fran1@jabb.im", body="Priprema") 
        await self.send(msg)
        msg = spade.message.Message(to="fran2@jabb.im", body="Priprema2") 
        await self.send(msg)
        msg = spade.message.Message(to="fran3@jabb.im", body="Kreni") 
        await self.send(msg)
        msg = spade.message.Message(to="fran4@jabb.im", body="Stop") 
        await self.send(msg)
        await sleep(2)
        self.set_next_state("PromijeniSmjer1")

class PromijeniSmjer1(State):
    async def run(self):
        
        print(colored('Promjena 1a', 'cyan'))
        msg = spade.message.Message(to="fran1@jabb.im", body="Kreni") 
        await self.send(msg)
        msg = spade.message.Message(to="fran3@jabb.im", body="Stop") 
        await self.send(msg)
        msg = spade.message.Message(to="fran2@jabb.im", body="Stop") 
        await self.send(msg)
        msg = spade.message.Message(to="fran4@jabb.im", body="Kreni") 
        await self.send(msg)
        await sleep(2)
        print(colored('Promjena 1b', 'magenta'))
        msg = spade.message.Message(to="fran1@jabb.im", body="Priprema2") 
        await self.send(msg)
        msg = spade.message.Message(to="fran2@jabb.im", body="Priprema") 
        await self.send(msg)
        await sleep(2)
        self.set_next_state("PromijeniSmjer2")

class PromijeniSmjer2(State):
    async def run(self):
        print(colored('Promjena 2a', 'cyan'))
        msg = spade.message.Message(to="fran1@jabb.im", body="Stop") 
        await self.send(msg)
        msg = spade.message.Message(to="fran3@jabb.im", body="Kreni") 
        await self.send(msg)
        msg = spade.message.Message(to="fran2@jabb.im", body="Kreni") 
        await self.send(msg)
        msg = spade.message.Message(to="fran4@jabb.im", body="Stop") 
        await self.send(msg)
        await sleep(2)
        print(colored('Promjena 2b', 'magenta'))
        msg = spade.message.Message(to="fran1@jabb.im", body="Priprema") 
        await self.send(msg)
        msg = spade.message.Message(to="fran2@jabb.im", body="Priprema2") 
        await self.send(msg)
        await sleep(2)
        self.set_next_state("PromijeniSmjer1")


class AgentUpravljac(Agent):
    async def setup(self):
        await sleep(2)
        print("UPRAVLJAC konacni automat krece u akciju!")


        fsm = PonasanjeKA1()

        fsm.add_state(name="PokreniRaskrizje", state=PokreniRaskrizje(), initial=True)
        fsm.add_state(name="PromijeniSmjer1", state=PromijeniSmjer1())
        fsm.add_state(name="PromijeniSmjer2", state=PromijeniSmjer2())

        fsm.add_transition(source="PokreniRaskrizje", dest="PromijeniSmjer1")
        fsm.add_transition(source="PromijeniSmjer1", dest="PromijeniSmjer2")
        fsm.add_transition(source="PromijeniSmjer2", dest="PromijeniSmjer1")

        self.add_behaviour(fsm)


if __name__ == '__main__':
    agentautomat1 = AgentAutomat1('fran1@jabb.im', '12345')
    agentautomat1.start()
    agentautomat2 = AgentAutomat2('fran2@jabb.im', '12345')
    agentautomat2.start()

    agentautomat3 = AgentAutomat3('fran3@jabb.im', '12345')
    agentautomat3.start()

    agentautomat4 = AgentAutomat4('fran4@jabb.im', '12345')
    agentautomat4.start()

    agentupravljac = AgentUpravljac('fran5@jabb.im', '12345')
    agentupravljac.start()

    input("Press ENTER to exit.\n")
    agentautomat1.stop()
    agentautomat2.stop()
    agentautomat3.stop()
    agentautomat4.stop()
    agentupravljac.stop()
    spade.quit_spade()
