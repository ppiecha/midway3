def sequencer_wrapper(music_args: MusicArgs):

    player_args = music_args.player.args[0]
    u2t = player_args.tick_from_unit
    track = music_args.voice
    soundfonts: Soundfonts = track.soundfonts_map_func()

    def seq_callback(time, event, seq, data):
        logger.debug(f"seq_callback: {time}, {event}, {seq}, {data}")
        schedule_next_bar(Tick(2.0).add(time))

    def schedule_next_callback(next_callback_time):
        # I want to be called back before the end of the next sequence
        logger.debug(f"schedule_next_callback: {next_callback_time}")
        sequencer.timer(next_callback_time, dest=my_seq_id)

    def schedule_next_bar(offset: Tick):
        logger.debug(f"schedule_next_bar: {offset}")
        tick, midi_events = events_from_sequences(music_args=music_args, offset=offset)
        for e in midi_events:
            logger.debug(f"{tick} {e}")
            sequencer_event(e)

        logger.debug(f"tt {tick} {offset} {Tick(tick / 2)} {Tick(tick / 2).add(offset)}")
        schedule_next_callback(Tick(tick / 2).add(offset))

    def sequencer_event(event: MidiEvent) -> None:
        match event.kind:
            case EventKind.NOTE:
                sequencer.note(
                    time=event.tick,
                    channel=event.channel,
                    key=event.key,
                    duration=event.duration,
                    velocity=event.velocity,
                    dest=synth_seq_id,
                )
            case EventKind.PROGRAM:
                sequencer.program_change(
                    time=event.tick,
                    channel=event.channel,
                    program=event.program,
                    dest=synth_seq_id,
                )
            case EventKind.CONTROL:
                sequencer.control_change(
                    time=event.tick,
                    channel=event.channel,
                    control=event.control.control,
                    value=event.control.value,
                    dest=synth_seq_id,
                )

    def load_soundfonts() -> SoundfontIds:
        return {
            name: fs.sfload(os.path.join(player_args.soundfont_path, file_name))
            for name, file_name in soundfonts.items()
        }

    fs = Synth()
    fs.start(driver="dsound")
    music_args = music_args._replace(soundfont_ids=load_soundfonts())
    sequencer = Sequencer(
        time_scale=ticks_per_second(player_args.bpm, player_args.ticks_per_beat), use_system_timer=False
    )
    synth_seq_id = sequencer.register_fluidsynth(fs)
    my_seq_id = sequencer.register_client("mycallback", seq_callback)
    schedule_next_bar(Tick(sequencer.get_tick()))
    time.sleep(20)
    logger.debug("starting to delete")
    sequencer.delete()
    fs.delete()
